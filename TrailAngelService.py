from TrailAngelFactory import TrailAngelFactory

class TrailAngelService:

    def __init__(self, db) -> None:
        self.trail_angel_factory = TrailAngelFactory()
        self.db = db

    def get_all_trail_angels(self):
        rows = self.db.get_trail_angels()
        trail_angels = self.trail_angel_factory.trail_angels_from_rows(rows)
        return trail_angels

    def get_trail_angel(self, trail_angel_id):
        row = self.db.get_trail_angel(trail_angel_id)
        if not row:
            raise Exception(f"Trail Angel Id [{trail_angel_id}] Not Found")
        trail_angel = TrailAngelFactory().trail_angel_from_row(row)
        return trail_angel

    def create_trail_angel(self, trail_angel):
        row = self.db.save_trail_angel(trail_angel)
        return self.trail_angel_factory.trail_angel_from_row(row)
