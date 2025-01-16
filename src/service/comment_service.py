from werkzeug.exceptions import BadRequest, NotFound
from data.database import Database
from domain.comment import Comment
from data.database import Database
from service.user_service import UserService
from service.post_service import PostService
from datetime import datetime


class CommentService:

    def __init__(
        self,
        db: Database,
        user_service: UserService,
        post_service: PostService
    ) -> None:
        self.db = db
        self.user_service = user_service
        self.post_service = post_service

    def create_comment(self, comment: Comment) -> Comment:

        self.post_service.get_post(comment.post_id)
        self.user_service.get_user(comment.user_id)

        comment.created_at = datetime.now()

        row = self.db.save_comment(comment)
        return self.__comment_from_row(row)

    def get_comments_for_post(self, id) -> list[Comment]:
        self.post_service.get_post(id)
        rows = self.db.get_comments_for_post(id)
        comments = []
        for row in rows:
            comments.append(self.__comment_from_row(row))
        comments.sort(key=lambda x: x.created_at)
        return comments

    def __comment_from_row(self, row) -> Comment:
        id, created_at, *args = row
        return Comment(*args, id=id, created_at=created_at)