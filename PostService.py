from Post import Post
from HikerService import HikerService
class PostService:

    def __init__(self, db) -> None:
        self.db = db

    def create_post(self, post):
        hiker = HikerService(self.db).get_hiker(post.hiker_id)

        if not hiker:
            raise Exception("Problem validating hiker creating post")
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





