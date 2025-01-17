class Comment:

    def __init__(self, user_id: str, post_id: str, text: str, created_at=None, id=None) -> None:
        self.id = id
        self.created_at = created_at
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
