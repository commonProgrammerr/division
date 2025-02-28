from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Role(SQLModel, table=True):
    name: Optional[str] = Field(nullable=False, primary_key=True)
    level: int = Field(nullable=False)
    description: str | None

    users: list["User"] = Relationship(back_populates="role")
