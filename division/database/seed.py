import os
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from division import models
from division.models.constraints import RoleLevel


def populate_database(engine: Engine):
    def add_admin(session: Session):
        if not (admin := session.get(models.User, 0)):
            admin = models.User(
                id=0,
                email="divisor_admin@poli.br",
                name="Divisor Admin",
                role=session.get(models.Role, RoleLevel.ADMIN.name),
                username=os.getenv("ADMIN_USER"),
                password=os.getenv("ADMIN_PASSWORD"),
            )
            session.add(admin)
            session.add(models.AccessKey(user=admin, value="2444"))

    def add_roles(session: Session):
        pass
        for role in RoleLevel:
            session.add(models.Role(name=role.name, level=role.value))

    with Session(engine) as session:
        add_roles(session)
        add_admin(session)
        session.commit()
