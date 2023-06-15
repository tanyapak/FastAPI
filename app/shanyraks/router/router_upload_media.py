from typing import List

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.shanyraks.adapters.s3_service import S3Service
from app.utils import AppModel
from fastapi import Depends, File, HTTPException, UploadFile

from ..service import Service, get_service
from . import router


class MediaUploadResponse(AppModel):
    detail: str


@router.post("/{shanyrak_id}/media", response_model=MediaUploadResponse)
def upload_shanyrak_media(
    shanyrak_id: str,
    files: List[UploadFile] = File(...),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    for file in files:
        # Generate the filename by combining the user_id and original filename
        filename = f"{jwt_data.user_id}_{file.filename}"

        # Upload the file to S3 and get the URL
        media_url = svc.s3_service.upload_file(file, filename)

        # Add the media URL to the shanyrak document
        update_result = svc.repository.add_shanyrak_media(shanyrak_id, jwt_data.user_id, media_url)

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Shanyrak not found")

    return MediaUploadResponse(detail="Media uploaded successfully")
