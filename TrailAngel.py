class TrailAngel:

    def __init__(self, first_name: str, last_name: str, location: str, capacity: int, cost: int, id = None) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.capacity = capacity
        self.cost = cost
