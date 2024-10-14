from Hiker import Hiker


class HikerService:

    def __init__(self, db) -> None:
        pass
        self.db = db

    def create_hiker(self, hiker):
        row = self.db.save_hiker(hiker)
        return self.hiker_from_row(row)

    def get_all_hikers(self):
        rows = self.db.get_hikers()
        return self.hikers_from_rows(rows)

    def hiker_from_row(self, row):
        return Hiker(row[0], row[1], row[2])

    def hikers_from_rows(self, rows):
        hikers = []
        for row in rows:
            hikers.append(self.hiker_from_row(row))
        return hikers
