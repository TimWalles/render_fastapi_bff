import uuid
from typing import List, Union

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.enums.Tables import Tables
from src.schemas.AggregatedScores import AggregatedScores, DailyScore
from src.schemas.DeleteResponse import DeleteResponse
from src.schemas.TotalScoreResponse import TotalScoreResponse, TotalUserScoreResponse
from src.services.data_database.tables import (
    Activity,
    ActivityCreate,
    ActivityUpdate,
    Reward,
    RewardCreate,
    RewardUpdate,
    Tracking,
    TrackingCreate,
    TrackingUpdate,
    TrackingWithActivityRead,
)
from src.utils import datetime_to_date, str_to_uuid, uuid_to_str

from .user import get_users


# region add data
async def add_data(
    session: Session,
    data: Union[RewardCreate, ActivityCreate, TrackingCreate],
) -> Reward | Activity | Tracking:
    try:
        match data:
            case RewardCreate():
                db_data = Reward.model_validate(data)
            case ActivityCreate():
                db_data = Activity.model_validate(data)
            case _:
                raise ValueError("Invalid data type")
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data already exists: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add data: {str(e)}",
        )


async def add_tracking(
    session: Session,
    data: TrackingCreate,
    user_id: str,
) -> Tracking:
    try:
        data = data.model_dump()
        data["user_id"] = uuid_to_str(user_id)
        db_data = Tracking.model_validate(data)
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data already exists: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add data: {str(e)}",
        )


# endregion


# region get data
async def get_data(
    session: Session,
    table: Tables,
) -> List[Union[Reward, Activity, Tracking]]:
    try:
        match table:
            case Tables.Rewards:
                statement = select(Reward)
            case Tables.Activity:
                statement = select(Activity)
            case Tables.Tracking:
                statement = select(Tracking)
            case _:
                raise ValueError("Invalid table type")
        return list(session.exec(statement).fetchall())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get data: {str(e)}",
        )


async def get_data_by_id(
    session: Session,
    table: Tables,
    id: str,
) -> List[Reward | Activity | Tracking]:
    try:
        match table:
            case Tables.Rewards:
                statement = select(Reward).where(Reward.id == id)
            case Tables.Activity:
                statement = select(Activity).where(Activity.id == id)
            case Tables.Tracking:
                statement = select(Tracking).where(Tracking.id == id)
            case _:
                raise ValueError("Invalid table type")
        return session.exec(statement)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get data: {str(e)}",
        )


async def get_user_activities(
    session: Session,
    user_id: str,
) -> List[Activity]:
    try:
        statement = select(Tracking).where(Tracking.user_id == user_id)
        data = session.exec(statement).fetchall()
        data = [TrackingWithActivityRead.model_validate(i) for i in data]
        return [i.activity for i in data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get user activities: {str(e)}",
        )


async def get_total_user_score(
    data_session: Session,
    user_session: Session,
    user_id: uuid.UUID,
) -> TotalUserScoreResponse:
    try:
        users = await get_users(session=user_session)
        if user_id not in [i.id for i in users]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        for i in users:
            if i.id == user_id:
                user = i
                break
        statement = select(Tracking).where(Tracking.user_id == user_id)
        data = data_session.exec(statement).fetchall()
        data = [TrackingWithActivityRead.model_validate(i) for i in data]
        return TotalUserScoreResponse(
            user=user,
            total_score=sum([i.activity.points for i in data]),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get total score: {str(e)}",
        )


async def get_user_daily_scores(
    data_session: Session,
    user_session: Session,
    user_id: uuid.UUID,
) -> AggregatedScores:
    try:
        users = await get_users(session=user_session)
        if user_id not in [i.id for i in users]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        for i in users:
            if i.id == user_id:
                user = i
                break
        statement = select(Tracking).where(Tracking.user_id == user_id)
        data = data_session.exec(statement).fetchall()
        data = [TrackingWithActivityRead.model_validate(i) for i in data]
        data.sort(key=lambda x: x.added_at, reverse=False)
        daily_scores = {}
        cumulative_score = 0
        for i in data:
            date = datetime_to_date(i.added_at)
            if date not in daily_scores:
                daily_scores[date] = 0
            daily_scores[date] += i.activity.points
        for i in daily_scores:
            cumulative_score += daily_scores[i]
            daily_scores[i] = DailyScore(date=i, score=daily_scores[i], cumulative_score=cumulative_score)
        daily_scores = list(daily_scores.values())
        return AggregatedScores(
            user_id=user_id,
            user_name=user.username,
            scores=daily_scores,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get daily scores: {str(e)}",
        )


async def get_total_scores(
    data_session: Session,
    user_session: Session,
) -> TotalScoreResponse:
    try:
        users = await get_users(session=user_session)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found",
            )
        total_scores = [
            await get_total_user_score(
                data_session=data_session,
                user_session=user_session,
                user_id=i.id,
            )
            for i in users
        ]
        total_scores.sort(key=lambda x: x.total_score, reverse=True)
        return TotalScoreResponse(users=total_scores)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get total score: {str(e)}",
        )


# endregion


# region update data
async def update_data(
    session: Session,
    table: Tables,
    id: str,
    data: Union[RewardUpdate, ActivityUpdate, TrackingUpdate],
) -> Reward | Activity | Tracking:
    try:
        db_data = (await get_data_by_id(session=session, table=table, id=id)).one_or_none()
        if db_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found",
            )
        data = data.model_dump(exclude_none=True)
        db_data.sqlmodel_update(data)
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Data already exists: {str(e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update data: {str(e)}",
        )


# endregion


# region delete data
async def delete_data(
    session: Session,
    table: Tables,
    id: str,
) -> DeleteResponse:
    try:
        match table:
            case Tables.Rewards:
                statement = select(Reward).where(Reward.id == id)
            case Tables.Activity:
                statement = select(Activity).where(Activity.id == id)
            case Tables.Tracking:
                statement = select(Tracking).where(Tracking.id == id)
            case _:
                raise ValueError("Invalid table type")
        db_data = session.exec(statement).one_or_none()
        if db_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found",
            )
        session.delete(db_data)
        session.commit()
        return DeleteResponse(
            id=id,
            message="Data deleted successfully",
            status="success",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete data: {str(e)}",
        )
