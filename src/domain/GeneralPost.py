from domain.UserType import UserType
from domain.Post import Post

class GeneralPost(Post):

    def __init__(self, user_id : str, user_type: UserType, title: str, text : str, id = None, created_at = None) -> None:
        Post.__init__(self, id=id, created_at=created_at, title=title, user_id=user_id, user_type=user_type)
        self.text = text
