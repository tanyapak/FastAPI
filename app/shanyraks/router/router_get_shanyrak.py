from typing import Any, List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from fastapi import Depends, Response
from pydantic import Field

from ..service import Service, get_service
from . import router


class GetShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    media: List[str]
    comments: List[Any]


@router.get("/{shanyrak_id:str}", response_model=GetShanyrakResponse)
def get_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, Any]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if shanyrak is None:
        return Response(status_code=404)

    # Convert ObjectId to string for user_id and media
    shanyrak["user_id"] = str(shanyrak.get("user_id"))
    shanyrak["media"] = [str(media) for media in shanyrak.get("media", [])]
    # shanyrak["comments"] = [str(value) for comment in shanyrak.get("comments", [])]

    return GetShanyrakResponse(**shanyrak)
