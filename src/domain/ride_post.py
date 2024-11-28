from domain.user_type import UserType
from domain.post import Post


class RidePost(Post):

    def __init__(
            self,
            user_id: str,
            user_type: UserType,
            title: str,
            pickup: str,
            dropoff: str,
            date: str,
            num_passengers: int,
            id=None,
            created_at=None
    ) -> None:
        Post.__init__(self, id=id, created_at=created_at,
                      title=title, user_id=user_id, user_type=user_type)
        self.pickup = pickup
        self.dropoff = dropoff
        self.date = date
        self.num_passengers = num_passengers
