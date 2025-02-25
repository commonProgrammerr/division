import os
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from division import models


def populate_database(engine: Engine):
    def add_admin(session: Session):
        find_admin = select(models.User).where(models.User.id == 0, models.User.username == "admin")
        if not (admin := session.exec(find_admin).first()):
            admin = models.User(
                id=0,
                email="divisor_admin@poli.br",
                name="Divisor Admin",
                role=session.exec(select(models.Role).where(models.Role.level == 0)).first(),
                username=os.getenv("ADMIN_USER"),
                password=os.getenv("ADMIN_PASSWORD"),
            )
            session.add(admin)
            session.add(models.AccessKey(user=admin))

    def add_roles(session: Session):
        for role in (
            {"name": "ADMIN", "level": 0},
            {"name": "STAFF", "level": 1},
            {"name": "STUDENT", "level": 10},
        ):
            session.add(models.Role(**role))

    with Session(engine) as session:
        add_roles(session)
        add_admin(session)
        session.commit()
