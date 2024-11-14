from RidePost import RidePost
from HikerService import HikerService
from TrailAngelService import TrailAngelService
from UserType import UserType
from data.database import Database

class RidePostService:

    def __init__(self, db: Database) -> None:
        self.db = db

    def create_ride_post(self, ride_post):

        user = None
        user_type = UserType(ride_post.user_type)

        if(user_type == UserType.HIKER):
            user = HikerService(self.db).get_hiker(ride_post.user_id)
        elif(user_type == UserType.TRAILANGEL):
            user = TrailAngelService(self.db).get_trail_angel(ride_post.user_id)
        else:
            raise Exception(f"User Type [{ride_post.user_type}] Undefined")

        if not user:
            raise Exception("Problem validating user creating post")

        row = self.db.save_ride_post(ride_post)
        return self.__ride_post_from_row(row)

    def get_ride_posts(self): 
        rows = self.db.get_ride_posts()
        return self.__ride_posts_from_rows(rows)

    def get_ride_post(self, ride_post_id):
        row = self.db.get_ride_post(ride_post_id)
        if not row:
            raise Exception(f"Ride Post Id [{ride_post_id}] Not Found")
        post = self.__ride_post_from_row(row)
        return post

    def delete_ride_post(self, ride_post_id):
        existing_ride_post = self.db.get_ride_post(ride_post_id)
        if not existing_ride_post:
            print(f"Attempted to delete nonexistent ride post [{ride_post_id}]")
            return
        self.db.delete_ride_post(ride_post_id)

    def __ride_posts_from_rows(self, rows):
        posts = []
        for row in rows:
            posts.append(self.__ride_post_from_row(row))
        return posts

    def __ride_post_from_row(self, row):
        id, *args = row
        return RidePost(*args, id = id)





