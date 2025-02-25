from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from division.utils.security import HashedPassword

if TYPE_CHECKING:
    from division.models.permissions import AccessKey, Role


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: int = Field(foreign_key="role.id", nullable=False)

    name: str | None = Field(nullable=True)
    username: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False)
    password: HashedPassword | None

    role: "Role" = Relationship(back_populates="users")
    keys: list["AccessKey"] = Relationship(back_populates="user")

    def __str__(self) -> str:
        return f"{self.name}"
