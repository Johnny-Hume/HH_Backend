class Comment:

    def __init__(self, post_id: str, user_id: str, text: str, created_at = None, id = None) -> None:
        self.id = id
        self.created_at = created_at
        self.post_id = post_id
        self.user_id = user_id
        self.text = text

