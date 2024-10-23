from TrailAngel import TrailAngel


class TrailAngelFactory:

    def __init__(self) -> None:
        pass

    def trail_angel_from_row(self, row):
        id = row[0]
        return TrailAngel(row[1], row[2], row[3], row[4], row[5], id)

    def trail_angels_from_rows(self, rows: list):
        angels = []
        for tuple in rows:
            angels.append(self.trail_angel_from_row(tuple))
        return angels
