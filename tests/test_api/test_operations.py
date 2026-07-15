from decimal import Decimal

from app.enum import CurrencyEnum
from app.models import User, Wallet


# Expense test
def test_add_expense_success(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "category": "food",
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["wallet_id"] == wallet.id
    assert payload["type"] == "expense"
    assert Decimal(payload["amount"]) == Decimal(50)
    assert payload["currency"] == CurrencyEnum.RUB
    assert payload["category"] == "food"
    assert payload["description"] == "food"

    db_session.refresh(wallet)
    assert wallet.balance == Decimal(150)


def test_add_expense_negative_amount(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 422


def test_add_expense_empty_name(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "    ",
            "amount": 100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 422


def test_add_expense_wallet_not_exist(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 404


def test_add_expense_unauthorized(client):
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer not exists"
        }
    )

    assert response.status_code == 401


def test_add_expense_not_enough_money(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 250.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 400


# Income tests
def test_add_income_success(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "category": "food",
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["wallet_id"] == wallet.id
    assert payload["type"] == "income"
    assert Decimal(payload["amount"]) == Decimal(50)
    assert payload["currency"] == CurrencyEnum.RUB
    assert payload["category"] == "food"
    assert payload["description"] == "food"

    db_session.refresh(wallet)
    assert wallet.balance == Decimal(250)


def test_add_income_negative_amount(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": -100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 422


def test_add_income_empty_name(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()

    wallet = Wallet(name='card', balance=200, user_id=user.id, currency=CurrencyEnum.RUB)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post(
        "api/v1/operations/income",
        json={
            "wallet_name": "    ",
            "amount": 100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 422


def test_add_income_wallet_not_exist(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    assert response.status_code == 404


def test_add_income_unauthorized(client):
    response = client.post(
        "api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food",
        },
        headers={
            "Authorization": f"Bearer not exists"
        }
    )

    assert response.status_code == 401
