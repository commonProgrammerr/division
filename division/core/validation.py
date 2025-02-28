from division.models import AccessKey, User
from division.models.constraints import AccessKeyType
from division.database import engine
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload


def get_access_key_by_value(key_type: AccessKeyType, key_value: str):
    with Session(engine) as session:
        query = (
            select(AccessKey)
            .options(joinedload(AccessKey.user).subqueryload(User.role))
            .where(
                AccessKey.type == key_type,
                AccessKey.value == key_value,
                AccessKey.enable == True,  # noqa: E712
            )
        )

        if not (key := session.exec(query).first()) or not key.enable:
            raise RuntimeError("Invalid AccessKey!")

        return key


def validate_unlock_request(key: AccessKey, lock_id: int):
    key.user.role.level
    pass
