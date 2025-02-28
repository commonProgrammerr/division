from enum import Enum
from sqlmodel import UniqueConstraint

unique_value_type_for_user = UniqueConstraint(
    "user_id", "value", "type", name="unique_value_type_for_user"
)


class AccessKeyType(Enum):
    CARD_ID = "card_id"
    FACE_ID = "face_ID"
    FINGERPRINT = "fingerprint"
    PASSWORD = "password"


class RoleLevel(Enum):
    ADMIN = 0
    STAFF = 5
    PROFESSOR = 10
    STUDENT = 20

    def __eq__(self, value):
        if isinstance(value, int):
            return self.value == value

        return super().__eq__(value)

    def __ge__(self, value):
        if isinstance(value, int):
            return self.value >= value

        return super().__eq__(value)

    def __gt__(self, value):
        if isinstance(value, int):
            return self.value > value
        return super().__eq__(value)

    def __le__(self, value):
        if isinstance(value, int):
            return self.value <= value

        return super().__eq__(value)

    def __lt__(self, value):
        if isinstance(value, int):
            return self.value < value
        return super().__eq__(value)
