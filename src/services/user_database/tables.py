import uuid
from typing import Optional

from sqlalchemy.orm import registry
from sqlmodel import Field, SQLModel

from src.enums.Roles import Roles


class UserBase(SQLModel, registry=registry()):
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None)
    user_avatar: Optional[str] = Field(default=None)
    user_country: Optional[str] = Field(default=None)
    team_name: Optional[str] = Field(default=None)
    job_name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    role: Roles = Field(default=Roles.User.value)
    hashed_password: str = Field()
    deactivated: bool = Field(default=False)


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
    deactivated: bool
    id: uuid.UUID


class UserRead(UserBase):
    id: uuid.UUID
    username: str
    email: Optional[str]
    user_avatar: Optional[str]
    user_country: Optional[str]
    team_name: Optional[str]
    job_name: Optional[str]


class UserUpdate(UserBase):
    username: str
    email: Optional[str]
    role: Roles
    deactivated: bool
    new_password: str
    user_avatar: Optional[str]
    user_country: Optional[str]
    team_name: Optional[str]
