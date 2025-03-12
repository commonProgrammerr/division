from typing import Optional

from sqlmodel import Field, SQLModel


class LocationString(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        elif not v:
            raise ValueError("Empty value is not acceptable")

        # removing double spaces
        return cls(" ".join(v.strip() for v in v.split(" ") if v))


class ZoneLock(SQLModel, table=True):
    id: Optional[int] = Field(nullable=True, primary_key=True)
    name: str
    location: LocationString | None = Field(nullable=True, index=True)
    level: int = Field(nullable=False)
    description: str | None
