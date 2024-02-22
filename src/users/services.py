from typing import Optional, Type

from sqlalchemy.orm import Session

from src.auth.config import bcrypt_context
from src.logger import logger
from src.users import models, schemas
from src.users.models import User
from src.users.schemas import UserDisplay


def get_user(db: Session, id: int) -> Optional[User]:
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserDisplay]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[UserDisplay]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserDisplay]]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> User:
    hashed_password = bcrypt_context.hash(user.password)
    logger.info(hashed_password)
    logger.info(user.password)
    db_user = models.User(email=user.email, username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
