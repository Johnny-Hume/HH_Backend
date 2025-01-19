from werkzeug.exceptions import NotFound
from domain.hiker import Hiker
from data.database import Database


class HikerService:

    def __init__(self, db: Database) -> None:
        pass
        self.db = db

    def create_hiker(self, hiker):
        row = self.db.save_hiker(hiker)
        return self.hiker_from_row(row)

    def get_all_hikers(self):
        rows = self.db.get_hikers()
        return self.hikers_from_rows(rows)

    def get_hiker(self, hiker_id):
        row = self.db.get_hiker(hiker_id)
        if not row:
            raise NotFound(f"Hiker Id [{hiker_id}] Not Found")
        hiker = self.hiker_from_row(row)
        return hiker

    def hiker_from_row(self, row):
        return Hiker(**row)

    def hikers_from_rows(self, rows):
        hikers = []
        for row in rows:
            hikers.append(self.hiker_from_row(row))
        return hikers
