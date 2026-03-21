from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enum import OperationType
from app.models import User
from app.repository import wallets as wallets_repository
from app.repository import operations as operations_repository
from app.schemas import OperationRequest, OperationResponse
from app.services.exchange_service import get_exchange_rate


def add_income(
        db: Session,
        current_user: User,
        operation: OperationRequest
    ) -> OperationResponse:
    """
    :param db:
    :param current_user:
    :param operation:
    :return: adds income operation
    """
    if not wallets_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.INCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    db.commit()
    return OperationResponse.model_validate(operation)


def add_expense(
        db: Session,
        current_user: User,
        operation: OperationRequest
    ) -> OperationResponse:
    """
    :param db:
    :param current_user:
    :param operation:
    :return: adds expense operation
    """
    if not wallets_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {wallet.balance}"
        )
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.EXPENSE,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    db.commit()
    return OperationResponse.model_validate(operation)


def get_operations_list(
        db: Session,
        current_user: User,
        wallet_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[OperationResponse]:
    """
    :param db:
    :param current_user:
    :param wallet_id:
    :param date_from:
    :param date_to:
    :return: returns the list of operations
    """
    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_id}' not found"
            )

        wallets_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        wallets_ids = [wallet.id for wallet in wallets]

    operations = operations_repository.get_operations_list(
        db=db,
        wallet_ids=wallets_ids,
        date_from=date_from,
        date_to=date_to
    )
    result = []
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))

    return result


async def transfer_between_wallets(
        db: Session,
        user_id: int,
        from_wallet_id: int,
        to_wallet_id: int,
        amount: Decimal,
    ) -> OperationResponse:
    """
    :param db:
    :param user_id:
    :param from_wallet_id:
    :param to_wallet_id:
    :param amount:
    :return: makes transfer between wallets
    """

    from_wallet = wallets_repository.get_wallet_by_id(db, user_id, from_wallet_id)
    to_wallet = wallets_repository.get_wallet_by_id(db, user_id, to_wallet_id)

    if not from_wallet or not to_wallet:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet not found"
        )

    if from_wallet.balance < amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {from_wallet.balance}"
        )

    target_amount = amount
    if from_wallet.currency != to_wallet.currency:
        exchange_rate = await get_exchange_rate(
            from_wallet.currency,
            to_wallet.currency,
        )
        target_amount = amount * exchange_rate

    from_wallet.balance = round(from_wallet.balance - amount, 2)
    to_wallet.balance = round(to_wallet.balance + target_amount, 2)
    operation = operations_repository.create_operation(
        db=db,
        wallet_id=from_wallet.id,
        type=OperationType.TRANSFER,
        amount=target_amount,
        currency=to_wallet.currency,
        category="transfer",
    )
    db.add(from_wallet)
    db.add(to_wallet)
    db.add(operation)
    db.commit()
    return OperationResponse.model_validate(operation)
