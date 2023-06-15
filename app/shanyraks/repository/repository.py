from datetime import datetime
from typing import Any, List, Optional

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

    def add_shanyrak_media(
        self, shanyrak_id: str, user_id: str, media_url: str
    ) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$push": {"media": media_url},
            },
        )

    def remove_all_shanyrak_media(self, shanyrak_id: str, user_id: str) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={"$set": {"media": []}},  # Reset the media list to be empty
        )

    def add_shanyrak_comment(
        self, shanyrak_id: str, comment: str, author_id: str
    ) -> Optional[ObjectId]:
        comment_id = ObjectId()

        comment_data = {
            "_id": comment_id,
            "content": comment,
            "created_at": datetime.now(),
            "author_id": author_id,
        }

        update_result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={"$push": {"comments": comment_data}},
        )

        if update_result.modified_count > 0:
            return comment_id

        return None
