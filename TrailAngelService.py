from TrailAngelFactory import TrailAngelFactory

from data.database import Database


class TrailAngelService:

    def __init__(self, db) -> None:
        self.trail_angel_factory = TrailAngelFactory()
        self.db = db

    def get_all_trail_angels(self):
        rows = self.db.get_trail_angels()
        angels = self.trail_angel_factory.trail_angels_from_rows(rows)
        return angels

    def get_trail_angel(self, angel_id):
        row = self.db.get_trail_angel(angel_id)
        angel = TrailAngelFactory().trail_angel_from_row(row)
        return angel

    def create_trail_angel(self, angel):
        row = self.db.save_trail_angel(angel)
        return self.trail_angel_factory.trail_angel_from_row(row)
