from typing import Optional, List
from sqlmodel import Session, select
from division.models import ZoneLock


def add_zone_lock(session: Session, lock_data: dict) -> ZoneLock:
    lock = ZoneLock(**lock_data)
    session.add(lock)
    return lock


def get_zone_lock(session: Session, lock_id: int) -> Optional[ZoneLock]:
    return session.get(ZoneLock, lock_id)


def update_zone_lock(session: Session, lock_id: int, lock_data: dict) -> Optional[ZoneLock]:
    if lock := get_zone_lock(session, lock_id):
        for key, value in lock_data.items():
            if key in lock.__annotations__:
                setattr(lock, key, value)
        session.add(lock)
    return lock


def delete_zone_lock(session: Session, lock_id: int) -> bool:
    if lock := get_zone_lock(session, lock_id):
        session.delete(lock)
        return True
    return False


def list_zone_locks(session: Session) -> List[ZoneLock]:
    statement = select(ZoneLock)
    return session.exec(statement).all()
