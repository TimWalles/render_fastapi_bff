from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.services.data_database.engine import DatabaseEngine as DataDatabaseEngine
from src.services.user_database.engine import DatabaseEngine as UserDatabaseEngine


# region get session
async def get_user_db_session(user_database_engine: Annotated[UserDatabaseEngine, Depends(UserDatabaseEngine)]):
    with Session(user_database_engine.engine) as session:
        yield session


async def get_data_db_session(database_engine: Annotated[DataDatabaseEngine, Depends(DataDatabaseEngine)]):
    with Session(database_engine.engine) as session:
        yield session


# endregion
