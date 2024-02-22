from pydantic import BaseModel
from typing import List


class CourseBase(BaseModel):
    title: str


class CourseCreate(CourseBase):
    pass


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class CourseDisplay(CourseBase):
    id: int
    users: List[UserBase] = []

    class Config:
        from_attributes = True


class UserDisplay(UserBase):
    id: int
    courses: List[CourseBase] = []

    class Config:
        from_attributes = True
