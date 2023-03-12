from services.interfaces.timeline_service_interface import Timeline_Service_Interface
from repos.orm.implementations.timeline_queries import Timeline_Repo
from datetime import datetime

class Timeline_Service(Timeline_Service_Interface):
    def __init__(self):
        self.timeline_repo = Timeline_Repo()

    def get_user_timeline(self, user_id, per_page_limit):
        return self.__format_time(self.timeline_repo.get_user_timeline(user_id, per_page_limit))

    def get_public_timeline(self, per_page_limit):
        return self.__format_time(self.timeline_repo.get_public_timeline(per_page_limit))

    def get_follower_timeline(self, username, per_page_limit):
        return self.__format_time(self.timeline_repo.get_follower_timeline(username, per_page_limit))

    def record_latest(self, latest):
        self.timeline_repo.record_latest(latest)

    def get_latest(self):
        return self.timeline_repo.get_latest()
    
    def __format_time(self, messages):
        if messages != None:
            for x in messages:
                x.date = datetime.fromtimestamp(x.pub_date).strftime("%H:%M:%S, %m/%d/%Y")
            return messages
        return []
