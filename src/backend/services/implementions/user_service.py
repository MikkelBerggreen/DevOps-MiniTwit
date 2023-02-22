from services.interfaces.user_service_interface import User_Service_Interface
from repos.implementations.user_repo import User_Repo

class User_Service(User_Service_Interface):

    def __init__(self):
        self.user_repo = User_Repo()

    def post_message(self, user_id, message):
        return self.user_repo.post_message(user_id,message)
    
    def remove_follower(self, user_id, follower_username):
        return self.user_repo.remove_follower(user_id,follower_username)

    def add_follower(self, user_id, follower_username):
        return self.user_repo.add_follower(user_id,follower_username)
    
    def get_all_followers(self, user_id, limit):
        return self.user_repo.get_all_followers(user_id,limit)
    
    def get_user_id_from_username(self, username):
        return self.user_repo.get_user_id_from_username(username)
