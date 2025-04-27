from typing import Optional

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.schemas.task import TaskStatus

class Base(DeclarativeBase):
    pass


class DBTask(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    status: Mapped[TaskStatus]
    due_date: Mapped[str]

