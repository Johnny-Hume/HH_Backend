from UserType import UserType

class Post:

    def __init__(
            self,
            title: str,
            user_id : str,
            user_type: UserType,
            id = None,
            created_at = None
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.user_id = user_id
        self.user_type = user_type
        self.title = title
