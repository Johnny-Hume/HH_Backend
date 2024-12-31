from domain.user_type import UserType
from dataclasses import dataclass


@dataclass
class Post:

    id: str | None
    created_at: str | None
    user_id: str
    user_type: UserType
    title: str
    text: str

    @classmethod
    def from_json(cls, json: dict):

        print(json)
        id = json.get("id")
        created_at = json.get("created_at")

        return Post(id, created_at, **json)
