from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from division.models.constraints import RoleLevel

if TYPE_CHECKING:
    from .user import User


class Role(SQLModel, table=True):
    name: Optional[str] = Field(nullable=False, primary_key=True)
    level: int = Field(nullable=False)
    description: str | None

    users: list["User"] = Relationship(back_populates="role")

    def __eq__(self, _in):
        if isinstance(_in, RoleLevel):
            return self.level == _in.value
        return super().__eq__(_in)

    def __ne__(self, _in):
        return not self.__eq__(_in)

    def __ge__(self, _in):
        if isinstance(_in, RoleLevel):
            return self.level >= _in.value
        return super().__ge__(_in)

    def __gt__(self, _in):
        if isinstance(_in, RoleLevel):
            return self.level > _in.value
        return super().__gt__(_in)

    def __le__(self, _in):
        if isinstance(_in, RoleLevel):
            return self.level <= _in.value
        return super().__le__(_in)

    def __lt__(self, _in):
        if isinstance(_in, RoleLevel):
            return self.level < _in.value
        return super().__lt__(_in)
