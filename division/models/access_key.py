from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from division.config import settings
from division.utils.security import HashedPassword
from .constraints import AccessKeyType

if TYPE_CHECKING:
    from division.models.user import User


def get_expiration_key_date(delta=timedelta(hours=settings.DEFAULT_EXPIRATION_TIME)):
    return datetime.utcnow() + delta


class AccessKey(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "value", "type", name="unique_value_type_for_user"),
    )

    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    type: AccessKeyType = Field(default=AccessKeyType.PASSWORD)
    value: HashedPassword = Field(index=True, nullable=False)

    enable: bool = Field(default=True)
    expiration: datetime = Field(default_factory=get_expiration_key_date)

    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="keys")
