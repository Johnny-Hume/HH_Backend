from dataclasses import dataclass


@dataclass
class User:

    id: str | None
    trail_name: str
    bio: str

    @classmethod
    def from_json(cls, json: dict):

        print(json)
        id = json.get("id")

        return User(id, **json)
