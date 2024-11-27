from werkzeug.exceptions import BadRequest, NotFound
from data.database import Database
from service.trail_angel_service import TrailAngelService
from service.hiker_service import HikerService
from domain.hiker import Hiker
from domain.trail_angel import TrailAngel
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
        user = self.__get_user_from_table(id)
        if not user:
            raise NotFound(f"User [{id}] Not Found")
        return user

    def get_users_names(self, ids: list[str]) -> dict[str, str]:
        names = {}

        for user_id in ids:
            try:
                user = self.__get_user_from_table(user_id)

                if isinstance(user, Hiker):
                    names[user_id] = user.trail_name
                elif isinstance(user, TrailAngel):
                    names[user_id] = f"{user.first_name} {user.last_name}"
            except (BadRequest, NotFound):
                print(f"Issue getting name for user [{user_id}]")
                pass

        return names

    def __get_user_from_table(self, user_id: str):
        table = user_id.split(self.db.id_delimiter)[0]
        
        if table == self.db.hikers_table:
            return self.hiker_service.get_hiker(user_id)
        elif table == self.db.trail_angels_table:
            return self.trail_angel_service.get_trail_angel(user_id)
        else:
            raise BadRequest(f"[{user_id}] Invalid user_id")
