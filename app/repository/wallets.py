from decimal import Decimal

from sqlalchemy.orm import Session

from app.enum import CurrencyEnum
from app.models import Wallet, User


def is_wallet_exists(
        db: Session,
        user_id: int,
        wallet_name: str
    ) -> bool:
    """
    :param db:
    :param user_id:
    :param wallet_name:
    :return: wallet exists
    """
    return db.query(Wallet).filter(
        Wallet.name == wallet_name, Wallet.user_id == user_id
    ).first() is not None


def add_income(
        db: Session,
        user_id: int,
        wallet_name: str,
        amount: Decimal
    ) -> Wallet:
    """
    :param db:
    :param user_id:
    :param wallet_name:
    :param amount:
    :return: updated wallet
    """
    wallet = db.query(Wallet).filter(
        Wallet.name == wallet_name, Wallet.user_id == user_id
    ).first()
    wallet.balance += amount
    return wallet


def get_wallet_balance_by_name(
        db: Session,
        user_id: int,
        wallet_name: str
    ) -> Wallet:
    """
    :param db:
    :param user_id:
    :param wallet_name:
    :return: balance
    """
    wallet = db.query(Wallet).filter(
        Wallet.name == wallet_name, Wallet.user_id == user_id
    ).first()
    return wallet


def add_expense(
        db: Session,
        user_id: int,
        wallet_name: str,
        amount: Decimal
    ) -> Wallet:
    """
    :param db:
    :param user_id:
    :param wallet_name:
    :param amount:
    :return: updated wallet
    """
    wallet = db.query(Wallet).filter(
        Wallet.name == wallet_name, Wallet.user_id == user_id
    ).first()
    wallet.balance -= amount
    return wallet


def get_all_wallets(
        db: Session,
        user_id: int
    ) -> list[Wallet]:
    """
    :param db:
    :param user_id:
    :return: gets wallets from db
    """
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_wallet(
        db: Session,
        user_id: int,
        wallet_name: str,
        amount: Decimal,
        currency: CurrencyEnum
    ) -> Wallet:
    """
    :param db:
    :param user_id:
    :param wallet_name:
    :param amount:
    :param currency:
    :return: created wallet
    """
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id, currency=currency)
    db.add(wallet)
    db.flush()
    return wallet


def get_wallet_by_id(
        db: Session,
        user_id: int,
        wallet_id: int
    ) -> Wallet | None:
    """
    :param db:
    :param user_id:
    :param wallet_id:
    :return: wallet or None
    """
    return db.query(Wallet).filter(
        Wallet.id == wallet_id, Wallet.user_id == user_id
    ).scalar()
