"""Database connection"""

from fastapi import Depends
from sqlmodel import Session, create_engine

from division.config.settings import DATABASE_URI
from division import models
from .seed import populate_database

engine = create_engine(
    DATABASE_URI,  # pyright: ignore
    echo=False,  # pyright: ignore
    # connect_args=settings.db.connect_args,  # pyright: ignore
)

models.SQLModel.metadata.create_all(bind=engine)

populate_database(engine)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)

__all__ = ["get_session", "engine", "ActiveSession"]
