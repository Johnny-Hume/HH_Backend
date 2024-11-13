from UserType import UserType

class Post:

    def __init__(self, title: str, user_id : str, user_type: UserType,pickup: str,dropoff: str,date: str, num_passengers: int, id = None) -> None:
        self.id = id
        self.user_id = user_id
        self.user_type = user_type
        self.title = title
        self.pickup = pickup
        self.dropoff = dropoff
        self.date = date
        self.num_passengers = num_passengers
