class Hiker:

    def __init__(self, trail_name: str, bio: str, id=None) -> None:
        self.id = id
        self.trail_name = trail_name
        self.bio = bio
