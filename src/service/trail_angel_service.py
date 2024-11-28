from werkzeug.exceptions import NotFound
from domain.trail_angel import TrailAngel


class TrailAngelService:

    def __init__(self, db) -> None:
        self.db = db

    def get_all_trail_angels(self):
        rows = self.db.get_trail_angels()
        trail_angels = self.trail_angels_from_rows(rows)
        return trail_angels

    def get_trail_angel(self, trail_angel_id):
        row = self.db.get_trail_angel(trail_angel_id)
        if not row:
            raise NotFound(f"Trail Angel Id [{trail_angel_id}] Not Found")
        trail_angel = self.trail_angel_from_row(row)
        return trail_angel

    def create_trail_angel(self, trail_angel):
        row = self.db.save_trail_angel(trail_angel)
        return self.trail_angel_from_row(row)

    def trail_angel_from_row(self, row):
        id = row[0]
        return TrailAngel(row[1], row[2], row[3], row[4], row[5], id)

    def trail_angels_from_rows(self, rows: list):
        angels = []
        for tuple in rows:
            angels.append(self.trail_angel_from_row(tuple))
        return angels
