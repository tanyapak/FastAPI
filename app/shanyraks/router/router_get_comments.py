from typing import Any, List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from fastapi import Depends, HTTPException, status
from pydantic import Field

from ..service import Service, get_service
from . import router


class CommentResponse(AppModel):
    _id: str = Field(alias="_id")
    content: str
    created_at: Any
    author_id: Any


@router.get("/{shanyrak_id}/comments", response_model=List[CommentResponse])
def get_shanyrak_comments(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)

    if not shanyrak:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shanyrak not found",
        )
    return shanyrak.get("comments", [])
