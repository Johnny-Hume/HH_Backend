from TrailAngel import TrailAngel


class TrailAngelFactory:

    def __init__(self) -> None:
        pass

    def trail_angel_from_tuple(self, tuple):
        return TrailAngel(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5])

    def trail_angels_from_tuples(self, tuples: list):
        angels = []
        for tuple in tuples:
            angels.append(self.trail_angel_from_tuple(tuple))
        return angels
