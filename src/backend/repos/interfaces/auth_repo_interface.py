from abc import ABCMeta, abstractmethod


class Auth_Repo_Interface:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def check_if_user_exists(self, username):
        raise NotImplementedError

    @abstractmethod
    def validate_user(self, username, password):
        raise NotImplementedError

    @abstractmethod
    def register_user(self, username, email, password):
        raise NotImplementedError