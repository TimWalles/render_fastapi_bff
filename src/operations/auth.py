import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from src.dependencies import *
from src.schemas.Token import TokenData
from src.services.user_database.tables import User
from src.settings import Settings, get_settings

from .user import get_user

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


async def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), bytes(hashed_password, "utf-8"))


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> bool:
    user = await get_user(session=session, username=username)
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(
    data: dict,
    settings: Settings,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)],
    settings: Annotated[Settings, Depends(get_settings)],
    session: AsyncSession = Depends(get_user_db_session),
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = await get_user(session, token_data.username)
    if not user:
        raise credential_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.deactivated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
