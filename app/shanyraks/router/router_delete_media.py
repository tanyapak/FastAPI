from typing import List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.shanyraks.adapters.s3_service import S3Service
from app.utils import AppModel
from fastapi import Depends, HTTPException, Response, status

from ..service import Service, get_service
from . import router


class MediaDeleteRequest(AppModel):
    media: List[str]


class MediaDeleteResponse(AppModel):
    detail: str


@router.delete("/{shanyrak_id}/media/all", response_model=MediaDeleteResponse)
def delete_all_shanyrak_media(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    s3_service: S3Service = Depends(S3Service),
):
    # Fetch the shanyrak media list
    media_list = svc.repository.get_shanyrak(shanyrak_id)

    for media_url in media_list:
        # Delete the file from S3
        s3_service.delete_file(media_url)

    # Remove all media URLs from the shanyrak document
    update_result = svc.repository.remove_all_shanyrak_media(shanyrak_id)

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shanyrak not found",
        )

    return MediaDeleteResponse(detail="Media deleted successfully")
