from UserType import UserType

class GeneralPost:

    def __init__(self, title: str, user_id : str, user_type: UserType, text : str, id = None) -> None:
        self.id = id
        self.user_id = user_id
        self.user_type = user_type
        self.title = title
        self.text = text
