from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import String, Enum, Text

from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class TodoStatus(str, PyEnum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    ARCHIVED = "archived"


class Todo(BaseModel):
    title: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus, name="user_status", native_enum=False),
        default=TodoStatus.NOT_STARTED,
        nullable=False,
    )
