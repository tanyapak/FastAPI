from typing import BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from fastapi import UploadFile


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, file: UploadFile, filename: str):
        bucket = "tatyana.r.pak-bucket"
        filekey = f"shanyraks/{filename}"

        # We first read the file to the memory, then pass the bytes to upload_fileobj
        self.s3.upload_fileobj(file.file, bucket, filekey)

        bucket_location = boto3.client("s3").get_bucket_location(Bucket=bucket)
        object_url = f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{bucket}/{filekey}"

        return object_url

    def delete_file(self, file_url: str) -> None:
        bucket = "tatyana.r.pak-bucket"
        file_key = file_url.split(bucket + "/")[-1]

        try:
            self.s3.delete_object(Bucket=bucket, Key=file_key)
        except BotoCoreError as e:
            print(f"An error occurred while trying to delete the file: {e}")
