from repos.interfaces.user_repo_interface import User_Repo_Interface
from database.db_util import Database

database = Database()


class User_Repo(User_Repo_Interface):
    def post_message(self, user_id, message):
        # To implement
        pass

    def remove_follower(self, user_id, follower_id):
        # To implement
        pass

    def add_follower(self, user_id, follower_id):
        # To implement
        pass

    def get_all_followers(self, user_id, limit):
        # To implement
        pass

    def get_user_id_from_username(self, username):
        # To implement
        pass

    def check_if_following(self, user_id, follower_id):
        # To implement
        pass