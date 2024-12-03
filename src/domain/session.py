class Session:
    def __init__(self, user_id: str, created_at: str, id=None) -> None:
        self.id = id
        self.created_at = created_at
        self.user_id = user_id
