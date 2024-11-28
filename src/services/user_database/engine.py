from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine

from src.services.user_database.tables import User
from src.settings import Settings, get_settings


async def init_user_db(settings: Annotated[Settings, Depends(get_settings)]) -> None:
    engine = create_engine(
        f"postgresql+pg8000://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.users_database_name}",
        # f"mysql+pymysql://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.users_database_name}",
        echo=False,
    )
    User.metadata.create_all(engine)


class DatabaseEngine:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]) -> None:
        self.engine = create_engine(
            f"postgresql+pg8000://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.users_database_name}",
            # f"mysql+pymysql://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.users_database_name}",
            echo=False,
        )
