from werkzeug.exceptions import BadRequest, NotFound
from data.database import Database
from domain.comment import Comment
from data.database import Database
from service.hiker_service import HikerService
from service.post_service import PostService
from service.ride_post_service import RidePostService
from service.trail_angel_service import TrailAngelService
from service.general_post_service import GeneralPostService
from datetime import datetime

class CommentService:

    def __init__(
        self,
        db: Database,
        hiker_service: HikerService,
        trail_angel_service: TrailAngelService,
        ride_post_service: RidePostService,
        general_post_service: GeneralPostService,
        post_service: PostService
    ) -> None:
        self.db = db
        self.hiker_service = hiker_service
        self.trail_angel_service = trail_angel_service
        self.ride_post_service = ride_post_service
        self.general_post_service = general_post_service
        self.post_service = post_service

    def create_comment(self, comment: Comment) -> Comment:

        self.__validate_user_id(comment)
        self.__validate_post_id(comment)

        comment.created_at = datetime.now()

        row = self.db.save_comment(comment)
        return self.__comment_from_row(row)

    def get_comments_for_post(self, id) -> list[Comment]:
        self.post_service.get_post(id)
        rows = self.db.get_comments_for_post(id)
        comments = []
        for row in rows:
            comments.append(self.__comment_from_row(row))
        return comments

    def __comment_from_row(self, row) -> Comment:
        id, created_at, *args = row
        return Comment(*args, id=id, created_at=created_at)

    def __validate_post_id(self, comment: Comment) -> None:
        self.post_service.get_post(comment.post_id)

    def __validate_user_id(self, comment: Comment) -> None:

        tables = {
            self.db.hikers_table: self.hiker_service.get_hiker,
            self.db.trail_angels_table: self.trail_angel_service.get_trail_angel
        }

        self.__validate_entity(comment.user_id, tables)

    def __validate_entity(self, id, tables):
        table_name = id.split(self.db.id_delimiter)[0]

        getter = tables.get(table_name, None)
        if not getter:
            raise BadRequest(f"Invalid Table [{id}]")

        entity = getter(id)

        if not entity:
            raise NotFound(f"[{id} Not Found]")

        return entity

