from services.interfaces.user_service_interface import User_Service_Interface
from repos.orm.implementations.user_queries import User_Repo
from util.custom_exceptions import Custom_Exception


class User_Service(User_Service_Interface):
    def __init__(self):
        self.user_repo = User_Repo()

    def post_message(self, user_id, message):
        return self.user_repo.post_message(user_id, message)

    def remove_follower(self, user_id, follower_username):
        follower_id = self.user_repo.get_user_id_from_username(follower_username)

        if follower_id is None:
            raise Custom_Exception(status_code=404,msg="User not found")

        return self.user_repo.remove_follower(user_id, follower_id)

    def add_follower(self, user_id, follower_username):
        follower_id = self.user_repo.get_user_id_from_username(follower_username)

        if follower_id is None:
            raise Custom_Exception(status_code=404,msg="User not found")

        return self.user_repo.add_follower(user_id, follower_id)

    def get_all_followers(self, user_id, limit):
        return self.user_repo.get_all_followers(user_id, limit)

    def get_user_id_from_username(self, username):

        user = self.user_repo.get_user_id_from_username(username)
        if user is None:
            raise Custom_Exception(status_code=404,msg="User not found")
        return user

    def check_if_following(self, user_id, follower_username):
        follower_id = self.user_repo.get_user_id_from_username(follower_username)

        if follower_id is None:
            raise Custom_Exception(status_code=404,msg="User not found")

        return self.user_repo.check_if_following(user_id, follower_id)
