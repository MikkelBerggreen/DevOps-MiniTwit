from abc import ABCMeta, abstractmethod


class Timeline_Service_Interface:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self):
        return "1.0"

    @abstractmethod
    def get_user_timeline(self, user_id, per_page_limit):
        raise NotImplementedError

    @abstractmethod
    def get_public_timeline(self, per_page_limit):
        raise NotImplementedError

    @abstractmethod
    def get_follower_timeline(self, username, per_page_limit):
        raise NotImplementedError

    @abstractmethod
    def record_latest(self, latest):
        raise NotImplementedError

    @abstractmethod
    def get_latest(self):
        raise NotImplementedError
