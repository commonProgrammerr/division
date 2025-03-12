from typing import Optional
from sqlmodel import Session
from division.models.access_key import AccessKey


def add_access_key(session: Session, access_key_data: dict):
    access_key = AccessKey(**access_key_data)
    session.add(access_key)
    return access_key


def get_access_key(session: Session, access_key_id: int) -> Optional[AccessKey]:
    return session.get(AccessKey, access_key_id)


def update_access_key(
    session: Session, access_key_id: int, access_key_data: dict
) -> Optional[AccessKey]:
    if access_key := get_access_key(session, access_key_id):
        for key, value in access_key_data.items():
            if key in access_key.__annotations__:
                setattr(access_key, key, value)
        session.add(access_key)
    return access_key


def delete_access_key(session: Session, access_key_id: int) -> bool:
    if access_key := session.get(AccessKey, access_key_id):
        session.delete(access_key)
        return True
    return False
