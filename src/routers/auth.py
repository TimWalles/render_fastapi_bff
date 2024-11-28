from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.operations.auth import authenticate_user, create_access_token
from src.schemas.Token import Token
from src.settings import Settings, get_settings

from ..dependencies import get_user_db_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    session: AsyncSession = Depends(get_user_db_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.access_token_expire_minutes))
    access_token = await create_access_token(
        data={"sub": user.username},
        settings=settings,
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="Bearer")
