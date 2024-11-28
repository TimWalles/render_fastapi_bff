import uuid
from typing import List

from pydantic import BaseModel

from src.services.user_database.tables import UserRead


class TotalUserScoreResponse(BaseModel):
    user: UserRead
    total_score: int


class TotalScoreResponse(BaseModel):
    users: List[TotalUserScoreResponse]
