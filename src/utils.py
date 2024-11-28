import uuid
from datetime import datetime


def uuid_to_str(uuid_: uuid.UUID) -> str:
    return str(uuid_)


def str_to_uuid(uuid_: str) -> uuid.UUID:
    return uuid.UUID(uuid_)


def datetime_to_date(datetime_: datetime) -> str:
    return datetime_.date().isoformat()
