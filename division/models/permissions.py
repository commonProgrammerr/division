import enum
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from division.config.settings import DEFAULT_EXPIRATION_TIME
from division.utils.auth import generate_password_key

if TYPE_CHECKING:
    from division.models import User


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    description: str | None
    level: int = Field(nullable=False)

    users: list["User"] = Relationship(back_populates="role")


class AccessKeyType(enum.Enum):
    CARD_ID = "card_id"
    FACE_ID = "face_ID"
    FINGERPRINT = "fingerprint"
    PASSWORD = "password"


def get_expiration_key_date(delta=timedelta(hours=DEFAULT_EXPIRATION_TIME)):
    return datetime.utcnow() + delta


class AccessKey(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "value", "type", name="unique_value_type_for_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    value: str = Field(index=True, default_factory=generate_password_key)
    expiration: datetime = Field(default_factory=get_expiration_key_date)
    type: AccessKeyType = Field(default=AccessKeyType.PASSWORD)
    enable: bool = Field(default=True)

    user: "User" = Relationship(back_populates="keys")
