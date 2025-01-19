from dataclasses import dataclass
import datetime


@dataclass
class Comment:

    id: str | None
    created_at: datetime.datetime | None
    post_id: str
    text: str
    user_id: str

    @classmethod
    def from_json(cls, json: dict):

        print(json)
        id = json.get("id")
        created_at = json.get("created_at")

        return Comment(id, created_at, **json)
