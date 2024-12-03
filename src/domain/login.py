class Login:

    def __init__(
        self,
        user_id: str,
        user_name: str,
        password: str,
        id: str | None = None,
        created_at: str | None = None
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
