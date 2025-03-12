from sqlmodel import Session

from division.database import engine
from .validation import get_key_by_value


def validate_key(**key):
    with Session(engine) as session:
        return get_key_by_value(session, **key)


def init_db():
    from division.database import models, engine
    from division.database.seed import populate_database

    models.SQLModel.metadata.create_all(bind=engine)
    populate_database(engine)
