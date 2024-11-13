from Post import Post
from HikerService import HikerService
from TrailAngelService import TrailAngelService
from UserType import UserType
class PostService:

    def __init__(self, db) -> None:
        self.db = db

    def create_post(self, post):

        user = None
        if(post.user_type == UserType.HIKER):
            user = HikerService(self.db).get_hiker(post.user_id)
        elif(post.user_type == UserType.TRAILANGEL):
            user = TrailAngelService(self.db).get_trail_angel(post.user_id)
        else:
            raise Exception("User Type Undefined")

        if not user:
            raise Exception("Problem validating user creating post")

        row = self.db.save_post(post)
        return self.__post_from_row(row)

    def get_posts(self): 
        rows = self.db.get_posts()
        return self.__posts_from_rows(rows)

    def get_post(self, post_id):
        row = self.db.get_post(post_id)
        if not row:
            raise Exception(f"Post Id [{post_id}] Not Found")
        post = self.__post_from_row(row)
        return post

    def delete_post(self, post_id):
        self.db.delete_post(post_id)

    def __posts_from_rows(self, rows):
        posts = []
        for row in rows:
            posts.append(self.__post_from_row(row))
        return posts

    def __post_from_row(self, row):

        id = row[0]
        hiker_id = row[1]
        title = row[2]
        pickup = row[3]
        dropoff = row[4]
        date = row[5]
        num_passengers = row[6]
        return Post(hiker_id, title, pickup, dropoff, date, num_passengers, id)





