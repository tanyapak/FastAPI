from typing import Any, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertManyResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    # def get_shanyrak(self, shanyrak_id: str):
    #     return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def get_shanyrak(self, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        if shanyrak is None:
            return None

        # Convert media from ObjectId to string
        shanyrak["media"] = [str(media) for media in shanyrak.get("media", [])]

        return shanyrak

    def update_shanyrak(
        self, shanyrak_id: str, user_id: str, data: dict[str, Any]
    ) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )

    def add_shanyrak_media(self, shanyrak_id: str, media_url: str) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$push": {"media": media_url},
            },
        )

    def remove_all_shanyrak_media(self, shanyrak_id: str) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$set": {
                    "media": []  # Reset the media list to be empty
                }
            },
        )
