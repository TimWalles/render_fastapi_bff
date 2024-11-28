from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, create_engine

from src.settings import Settings, get_settings

from . import tables


async def init_db(settings: Annotated[Settings, Depends(get_settings)]) -> None:
    engine = create_engine(
        f"postgresql+pg8000://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.data_database_name}",
        # f"mysql+pymysql://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.data_database_name}",
        echo=False,
    )
    SQLModel.metadata.create_all(engine, checkfirst=True)


class DatabaseEngine:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.engine = create_engine(
            f"postgresql+pg8000://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.data_database_name}",
            # f"mysql+pymysql://{settings.database_user}:{settings.database_password}@{settings.database_domain}/{settings.data_database_name}",
            pool_size=20,
            max_overflow=10,
            echo=False,
            pool_recycle=3600,
        )
