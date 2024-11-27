from werkzeug.exceptions import BadRequest, NotFound
from data.database import Database
from service.ride_post_service import RidePostService
from service.general_post_service import GeneralPostService
from domain.general_post import GeneralPost
from domain.ride_post import RidePost

class PostService:

    def __init__(self, db: Database, rps: RidePostService, gps: GeneralPostService) -> None:
        self.db = db
        self.ride_service = rps
        self.general_service = gps

    def get_all_posts(self):
        ride_posts = self.ride_service.get_ride_posts()
        general_posts = self.general_service.get_general_posts()

        merged = ride_posts + general_posts
        merged.sort(key=lambda post: post.created_at)
        return merged

    def get_post(self, id) -> RidePost | GeneralPost:

        table_name = id.split(self.db.id_delimiter)[0]

        post = None
        if table_name == self.db.ride_posts_table:
            post = self.ride_service.get_ride_post(id)
        elif table_name == self.db.general_posts_table:
            post = self.general_service.get_general_post(id)
        else:
            raise BadRequest(f"Invalid PostId [{id}]")

        if not post:
            raise NotFound(f"Post [{id}] Not Found")

        return post

