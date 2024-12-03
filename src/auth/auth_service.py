import datetime
from data.database import Database
from werkzeug import exceptions
from datetime import datetime
from domain.session import Session
from domain.login import Login


class AuthService:

    def __init__(self, db: Database) -> None:
        self.db = db
        self.SESSION_TIMEOUT_MINUTES = 60

    def login_user(self, login) -> Session:
        if not login.user_name:
            raise exceptions.BadRequest("Username not present in request")

        row = self.db.get_login_for_user(login.user_name)

        if not row:
            raise exceptions.NotFound("That Username/Password was not found")

        id, created_at, *args = row

        stored_login = Login(*args, id=id, created_at=created_at)

        if stored_login.password != login.password:
            raise exceptions.NotFound("That Username/Password was not found")

        session = Session(stored_login.user_id, str(datetime.now()))

        id, *args = self.db.save_session(session)

        session.id = id

        return session
