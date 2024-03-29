from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone

from src.database import get_db
from src.auth.constants import (
    ACCESS_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    REFRESH_SECRET_KEY,
)
from src.auth.schemas import TokenData
from src.auth.config import bcrypt_context, oauth2_bearer
from src.logger import logger
from src.users.schemas import UserDisplay
from src.users.services import get_user_by_username
from src.users.models import User


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return bcrypt_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_date: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_date:
        expire = datetime.now(timezone.utc) + expires_date
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "sub": data["sub"]})
    encoded_jwt = jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_date: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_date:
        expire = datetime.now(timezone.utc) + expires_date
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "sub": data["sub"]})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
