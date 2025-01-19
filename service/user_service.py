from werkzeug.exceptions import NotFound
from domain.user import User
from data.database import Database


class UserService:

    def __init__(self, db: Database) -> None:
        pass
        self.db = db

    def create_user(self, user):
        row = self.db.save_user(user)
        return self.user_from_row(row)

    def get_all_users(self):
        rows = self.db.get_users()
        return self.users_from_rows(rows)

    def get_user(self, id):
        row = self.db.get_user(id)
        if not row:
            raise NotFound(f"User Id [{id}] Not Found")
        user = self.user_from_row(row)
        return user

    def user_from_row(self, row):
        id = row[0]
        trail_name = row[1]
        bio = row[2]
        return User(id=id, trail_name=trail_name, bio=bio)

    def users_from_rows(self, rows):
        users = []
        for row in rows:
            users.append(self.user_from_row(row))
        return users


    def get_users_names(self, ids: list[str]) -> dict[str, str]:
        names = {}

        for user_id in ids:
            user = self.get_user(user_id)
            names[user_id] = user.trail_name

        return names