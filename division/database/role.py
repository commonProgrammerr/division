from typing import Optional
from sqlmodel import Session
from division.models.role import Role


def add_role(session: Session, role_data: dict):
    role = Role(**role_data)
    session.add(role)
    return role


def get_role(session: Session, role_name: str) -> Optional[Role]:
    return session.get(Role, role_name)


def update_role(session: Session, role_name: str, role_data: dict) -> Optional[Role]:
    if role := get_role(session, role_name):
        for key, value in role_data.items():
            if key in role.__annotations__:
                setattr(role, key, value)
        session.add(role)
    return role


def delete_role(session: Session, role_name: str) -> bool:
    if role := get_role(session, role_name):
        session.delete(role)
        return True
    return False
