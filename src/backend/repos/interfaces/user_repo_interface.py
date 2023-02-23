from abc import ABCMeta, abstractmethod


class User_Repo_Interface:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def post_message(self, user_id, message):
        raise NotImplementedError

    @abstractmethod
    def remove_follower(self, user_id, follower_username):
        raise NotImplementedError

    @abstractmethod
    def add_follower(self, user_id, follower_username):
        raise NotImplementedError
    
    @abstractmethod
    def get_all_followers(self, user_id, limit):
        raise NotImplementedError
    
    @abstractmethod
    def get_user_id_from_username(self, username):
        raise NotImplementedError
    
    @abstractmethod
    def check_if_following( self, user_id, follower_username):
        raise NotImplementedError