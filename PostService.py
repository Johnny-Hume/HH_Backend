from RidePostService import RidePostService
from GeneralPostService import GeneralPostService

class PostService:

    def __init__(self, rps: RidePostService, gps: GeneralPostService) -> None:
        self.ride_service = rps
        self.general_service = gps

    def get_all_posts(self):
        ride_posts = self.ride_service.get_ride_posts()
        general_posts = self.general_service.get_general_posts()

        merged = ride_posts + general_posts
        merged.sort(key=lambda post: post.created_at)
        return merged

