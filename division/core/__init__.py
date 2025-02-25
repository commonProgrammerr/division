from division.models import AccessKey, AccessKeyType

from division.database import engine
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload


def validate_access_key(key_type: AccessKeyType, key_value: str):
    with Session(engine) as session:
        query = (
            select(AccessKey)
            .options(selectinload(AccessKey.user))
            .where(AccessKey.type == key_type, AccessKey.value == key_value)
        )

        if not (key := session.exec(query).first()) or not key.enable:
            raise RuntimeError("Invalid AccessKey!")

        return key
