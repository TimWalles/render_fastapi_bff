from typing import List

import bcrypt
from sqlmodel import Session, select

from src.services.user_database.tables import User, UserCreate, UserInDB, UserRead


async def get_hashed_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


async def create_new_user(
    session: Session,
    user: UserCreate,
) -> UserRead:

    hashed_password = {"hashed_password": await get_hashed_password(user.password)}
    db_user = User.model_validate(user, update=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return UserRead.model_validate(db_user)


async def get_user(
    session: Session,
    username: str,
) -> UserInDB | None:
    result = session.exec(select(User).where(User.username == username))
    user_data = result.first()
    if user_data and user_data.username.lower() == username.lower():
        return UserInDB.model_validate(user_data)
    return None


async def get_users(
    session: Session,
) -> List[UserRead] | None:
    statement = select(User)
    result = session.exec(statement)
    return [UserRead.model_validate(user) for user in result]
