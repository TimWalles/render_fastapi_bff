import uuid
from typing import Annotated, List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlmodel import Session

from src.dependencies import get_data_db_session, get_user_db_session
from src.enums.Tables import Tables
from src.operations.auth import get_current_active_user
from src.operations.data import (
    add_data,
    add_tracking,
    delete_data,
    get_data,
    get_total_scores,
    get_total_user_score,
    get_user_activities,
    get_user_daily_scores,
    update_data,
)
from src.schemas.AggregatedScores import AggregatedScores
from src.schemas.DeleteResponse import DeleteResponse
from src.schemas.TotalScoreResponse import TotalScoreResponse, TotalUserScoreResponse
from src.services.data_database.tables import (
    ActivityCreate,
    ActivityRead,
    ActivityUpdate,
    RewardCreate,
    RewardRead,
    RewardUpdate,
    TrackingCreate,
    TrackingUpdate,
    TrackingWithActivityRead,
)
from src.services.user_database.tables import User

disable_installed_extensions_check()

router = APIRouter(prefix="/data", tags=["data"])


# region get routes
@router.get(
    "/{table}/all",
    response_model=Page[
        Union[
            RewardRead,
            ActivityRead,
            TrackingWithActivityRead,
        ]
    ],
    status_code=status.HTTP_200_OK,
    summary="Get all rewards",
)
async def get_table_data(
    table: Tables,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        response = await get_data(
            session=session,
            table=table,
        )
        return paginate(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/total_score/{user_id}/get",
    response_model=TotalUserScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Get total score of user",
)
async def get_user_score(
    user_id: uuid.UUID,
    user_session: Session = Depends(get_user_db_session),
    data_session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await get_total_user_score(
            data_session=data_session,
            user_session=user_session,
            user_id=user_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/total_score/get",
    response_model=Page[TotalScoreResponse],
    status_code=status.HTTP_200_OK,
    summary="Get total score of all users",
)
async def get_total_score(
    data_session: Session = Depends(get_data_db_session),
    user_session: Session = Depends(get_user_db_session),
    current_user: User = Depends(get_current_active_user),
    params: Params = Depends(),
):
    try:
        response = await get_total_scores(
            data_session=data_session,
            user_session=user_session,
        )
        return paginate(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/tracking/{user_id}/get",
    response_model=Page[ActivityRead],
    status_code=status.HTTP_200_OK,
    summary="Get all tracking of user",
)
async def get_user_tracking(
    user_id: uuid.UUID,
    session: Session = Depends(get_data_db_session),
    params: Params = Depends(),
    current_user: User = Depends(get_current_active_user),
):
    try:
        response = await get_user_activities(
            session=session,
            user_id=user_id,
        )
        return paginate(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/tracking/{user_id}/aggregate",
    response_model=AggregatedScores,
    status_code=status.HTTP_200_OK,
    summary="Get all tracking of user",
)
async def get_daily_scores(
    user_id: uuid.UUID,
    data_session: Session = Depends(get_data_db_session),
    user_session: Session = Depends(get_user_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await get_user_daily_scores(
            data_session=data_session,
            user_session=user_session,
            user_id=user_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region post routes
@router.post(
    "/reward/add",
    response_model=RewardRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new reward",
)
async def create_reward(
    reward: RewardCreate,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await add_data(
            session=session,
            data=reward,
        )
        return {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/activity/add",
    response_model=ActivityRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new reward",
)
async def create_activity(
    reward: ActivityCreate,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await add_data(
            session=session,
            data=reward,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/tracking/add",
    response_model=TrackingWithActivityRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add new activity to user",
)
async def create_activity(
    reward: TrackingCreate,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await add_tracking(
            session=session,
            data=reward,
            user_id=current_user.id,
        )
        return {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion


# region patch routes\
@router.patch(
    "/reward/{reward_id}/update",
    response_model=RewardRead,
    status_code=status.HTTP_200_OK,
    summary="Update reward",
)
async def update_reward(
    reward_id: uuid.UUID,
    data: RewardUpdate,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await update_data(
            session=session,
            table=Tables.Rewards,
            data=data,
            id=reward_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/activity/{activity_id}/update",
    response_model=ActivityRead,
    status_code=status.HTTP_200_OK,
    summary="Update activity",
)
async def update_reward(
    activity_id: uuid.UUID,
    data: ActivityUpdate,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await update_data(
            session=session,
            table=Tables.Activity,
            data=data,
            id=activity_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion

# region delete routes


@router.delete(
    "/reward/{reward_id}/delete",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
    summary="Delete reward",
)
async def delete_reward(
    reward_id: uuid.UUID,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await delete_data(
            session=session,
            table=Tables.Rewards,
            id=reward_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/activity/{activity_id}/delete",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
    summary="Delete activity",
)
async def delete_activity(
    activity_id: uuid.UUID,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await delete_data(
            session=session,
            table=Tables.Activity,
            id=activity_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/tracking/{tracking_id}/delete",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
    summary="Delete tracking",
)
async def delete_tracking(
    tracking_id: uuid.UUID,
    session: Session = Depends(get_data_db_session),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await delete_data(
            session=session,
            table=Tables.Tracking,
            id=tracking_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# endregion
