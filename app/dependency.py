from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Generator
from app.database import SessionLocal
from app.models import User
from app.repository import users as user_repository


security = HTTPBearer()

def get_db() -> Generator[Session, None, None]:
    """
    Get db session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> User:
    """
    Get current user
    :param credentials:
    :param db:
    :return: user
    """
    login = credentials.credentials

    user = user_repository.get_user(db, login)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return user