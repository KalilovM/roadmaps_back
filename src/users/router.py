from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated
from sqlalchemy.orm import Session

from src.auth.services import get_current_user
from src.logger import logger
from src.users import schemas, services
from src.database import get_db
from src.users.schemas import UserDisplay

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/", response_model=schemas.UserDisplay)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username is already registered")
    return services.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.UserDisplay])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip, limit)
    return users


@router.get("/me", response_model=schemas.UserDisplay)
async def read_users_me(current_user=Depends(get_current_user)):
    return UserDisplay.from_orm(current_user)


@router.get("/{user_id}", response_model=schemas.UserDisplay)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
