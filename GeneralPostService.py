from data.database import Database
from GeneralPost import GeneralPost
from datetime import datetime

class GeneralPostService:

    def __init__(self, db: Database) -> None:
        self.db = db

    def get_general_posts(self):
        rows = self.db.get_general_posts()
        general_posts = []
        for row in rows:
            general_posts.append(self.__general_post_from_row(row))
        return general_posts

    def create_general_post(self, general_post: GeneralPost):

        now = datetime.now()
        general_post.created_at = str(now)

        row = self.db.save_general_post(general_post)
        return self.__general_post_from_row(row)

    def __general_post_from_row(self, row: tuple):
        id, created_at, *args = row
        return GeneralPost(*args, id=id, created_at=created_at)
