from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from sqlalchemy.orm import Session

from src.auth.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_SECRET_KEY,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from src.auth.schemas import Token, AccessToken
from src.auth.services import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)
from src.auth.config import oauth2_bearer
from src.database import get_db
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_date=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_date=refresh_token_expires
    )
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=AccessToken)
async def refresh_token(refresh_token: str = Depends(oauth2_bearer)) -> Token:
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    new_access_token = create_access_token(data={"sub": username})
    return AccessToken(access_token=new_access_token, token_type="bearer")
