from __future__ import annotations

from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from typing import List


# mapped_column


class Base(DeclarativeBase):
    pass


user_course_table = Table('user_course', Base.metadata,
                          Column("user_id", Integer, ForeignKey('user.id'), primary_key=True),
                          Column("course_id", Integer, ForeignKey("course.id"), primary_key=True))


class User(Base):
    __tablename__ = "user"

    # TODO: change to UUID
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    courses: Mapped[List[Course]] = relationship("Course", secondary=user_course_table, back_populates="users")


class Course(Base):
    __tablename__ = "course"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String, index=True)
    users:Mapped[List[User]] = relationship(
        "User",
        secondary=user_course_table,
        back_populates="courses"
    )
