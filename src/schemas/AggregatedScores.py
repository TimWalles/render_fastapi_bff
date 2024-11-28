import uuid
from datetime import date

from pydantic import BaseModel


class DailyScore(BaseModel):
    date: date
    score: int
    cumulative_score: int


class AggregatedScores(BaseModel):
    user_id: uuid.UUID
    user_name: str
    scores: list[DailyScore]
