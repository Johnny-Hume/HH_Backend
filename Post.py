class Post:

    def __init__(self, hiker_id: int, title: str,pickup: str,dropoff: str,date: str, num_passengers: int, id = None) -> None:
        self.id = id
        self.hiker_id = hiker_id
        self.title = title
        self.pickup = pickup
        self.dropoff = dropoff
        self.date = date
        self.num_passengers = num_passengers
