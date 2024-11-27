from werkzeug.exceptions import BadRequest, NotFound
from data.database import Database
from service.trail_angel_service import TrailAngelService
from service.hiker_service import HikerService
class UserService:

    def __init__(
            self,
            db: Database,
            trail_angel_service: TrailAngelService,
            hiker_service: HikerService
    ) -> None:
        self.db = db
        self.trail_angel_service = trail_angel_service
        self.hiker_service = hiker_service

    def get_user(self, id):
        table = id.split(self.db.id_delimiter)[0]
        user = None
        print(table)
        if table == self.db.hikers_table:
            user = self.hiker_service.get_hiker(id)
        elif table == self.db.trail_angels_table:
            user = self.trail_angel_service.get_trail_angel(id)
        else:
            raise BadRequest(f"[{id}] Invalid user_id")

        if not user:
            raise NotFound(f"User [{id}] Not Found")
        return user

