from werkzeug.exceptions import NotFound
from data.database import Database
from domain.post import Post
from datetime import datetime


class PostService:

    def __init__(self, db: Database) -> None:
        self.db = db

    def get_posts(self):
        rows = self.db.get_posts()
        posts = []
        for row in rows:
            posts.append(self.__post_from_row(row))
        posts.sort(key=lambda post: post.created_at)
        return posts

    def get_post(self, post_id):
        row = self.db.get_post(post_id)
        if not row:
            raise NotFound(f"Post [{post_id}] Not Found")
        post = self.__post_from_row(row)
        return post

    def create_post(self, post: Post):

        now = datetime.now()
        post.created_at = str(now)

        row = self.db.save_post(post)
        print(row)
        return self.__post_from_row(row)

    def __post_from_row(self, row: list):
        return Post(*row)
