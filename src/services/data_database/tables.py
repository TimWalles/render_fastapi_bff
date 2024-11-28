import uuid
from datetime import UTC, datetime, timedelta
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# region Rewards
class RewardBase(SQLModel):
    name: str = Field(nullable=False)
    points: int = Field(nullable=False)


class Reward(RewardBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)


class RewardCreate(RewardBase):
    pass


class RewardRead(RewardBase):
    id: uuid.UUID


class RewardUpdate(SQLModel):
    name: Optional[str] = None
    points: Optional[int] = None


# endregion


# region Activity
class ActivityBase(SQLModel):
    name: str = Field(nullable=False)
    points: int = Field(nullable=False)


class Activity(ActivityBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    tracking: List["Tracking"] = Relationship(back_populates="activity", cascade_delete=True)


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: uuid.UUID


class ActivityUpdate(SQLModel):
    name: Optional[str] = None
    points: Optional[int] = None


# endregion


class TrackingBase(SQLModel):
    activity_id: uuid.UUID = Field(nullable=False, foreign_key="activity.id", ondelete="CASCADE")


class Tracking(TrackingBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    added_at: datetime = Field(default=datetime.now(UTC) - timedelta(days=1), nullable=False)
    user_id: Optional[uuid.UUID] = Field(primary_key=True, nullable=False)
    activity: Activity = Relationship(back_populates="tracking")


class TrackingCreate(TrackingBase):
    pass


class TrackingRead(TrackingBase):
    id: uuid.UUID
    user_id: uuid.UUID
    added_at: datetime


class TrackingUpdate(SQLModel):
    activity_id: Optional[uuid.UUID] = None


class TrackingWithActivityRead(TrackingRead):
    activity: ActivityRead


# endregion
