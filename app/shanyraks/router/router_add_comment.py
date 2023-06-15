from typing import Optional

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from fastapi import Depends, HTTPException, status

from ..service import Service, get_service
from . import router


@router.post("/{shanyrak_id}/comments", status_code=status.HTTP_201_CREATED)
def add_shanyrak_comment(
    shanyrak_id: str,
    comment: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    # Add the comment to the shanyrak document
    comment_id = svc.repository.add_shanyrak_comment(
        shanyrak_id, comment, jwt_data.user_id
    )

    if not comment_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shanyrak not found",
        )

    return {"detail": "Comment added successfully", "comment_id": str(comment_id)}
