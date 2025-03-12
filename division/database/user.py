from typing import Optional
from division.models import User
from division.models.user import generate_username
from sqlmodel import Session


def add_user(session: Session, user_data: dict):
    if "username" not in user_data and "name" in user_data:
        user_data["username"] = generate_username(user_data["name"])

    user = User(**user_data)
    session.add(user)
    return user


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def update_user(session: Session, user_id: int, user_data: dict) -> Optional[User]:
    if user := get_user(session, user_id):
        for key, value in user_data.items():
            if key in user.__annotations__:
                setattr(user, key, value)
        session.add(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    if user := session.get(User, user_id):
        session.delete(user)
        return True
    return False
