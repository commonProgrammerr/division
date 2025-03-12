"""Database connection"""

from fastapi import Depends
from sqlmodel import Session, create_engine

from division.config import settings
from division import models
from . import user, role, access_key, lock

engine = create_engine(
    settings.DATABASE_URI,  # pyright: ignore
    echo=False,  # pyright: ignore
    # connect_args=settings.db.connect_args,  # pyright: ignore
)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)

__all__ = ["get_session", "engine", "ActiveSession", "user", "role", "access_key", "lock", "models"]
