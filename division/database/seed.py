import os
from typing import Callable, Any
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from division import models

from division.database.access_key import add_access_key
from division.database.lock import add_zone_lock
from division.database.user import add_user
from division.models.constraints import RoleLevel
from csv import reader

SEEDS = (
    ("USER_SEED", add_user),
    ("ZONELOCK_SEED", add_zone_lock),
    ("ACCESSKEY_SEED", add_access_key),
)


def populate_table(session: Session, seed: str, seeder: Callable[[Session, dict], Any]):
    population = reader(open(seed))
    headers = []
    for i, entity in enumerate(population):
        if i == 0:
            for attr in entity:
                headers.append(str.strip(attr))
        else:
            data = dict(zip(headers, map(str.strip, entity)))
            seeder(session, data)


def update_roles(session: Session):
    roles = session.exec(select(models.Role.name)).all()
    for role in RoleLevel:
        if role.name not in roles:
            session.add(models.Role(name=role.name, level=role.value))


def populate_database(engine: Engine):
    with Session(engine) as session:
        update_roles(session)
        for seed, seeder in SEEDS:
            if seed_file := os.getenv(seed):
                populate_table(session, seed_file, seeder)

        session.commit()
