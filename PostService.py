from Post import Post
class PostService:

    def __init__(self, db) -> None:
        self.db = db

    def create_post(self, post):
        row = self.db.save_post(post)
        return self.post_from_row(row)

    def post_from_row(self, row):

        id = row[0]
        hiker_id = row[1]
        title = row[2]
        pickup = row[3]
        dropoff = row[4]
        date = row[5]
        num_passengers = row[6]
        return Post(hiker_id, title, pickup, dropoff, date, num_passengers, id)





