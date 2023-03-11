from services.interfaces.timeline_service_interface import Timeline_Service_Interface
from repos.orm.implementations.timeline_queries import Timeline_Repo


class Timeline_Service(Timeline_Service_Interface):
    def __init__(self):
        self.timeline_repo = Timeline_Repo()

    def get_user_timeline(self, user_id, per_page_limit):
        return self.timeline_repo.get_user_timeline(user_id, per_page_limit)

    def get_public_timeline(self, per_page_limit):
        return self.timeline_repo.get_public_timeline(per_page_limit)

    def get_follower_timeline(self, username, per_page_limit):
        return self.timeline_repo.get_follower_timeline(username, per_page_limit)

    def record_latest(self, latest):
        self.timeline_repo.record_latest(latest)

    def get_latest(self):
        return self.timeline_repo.get_latest()
