from repos.interfaces.timeline_repo_interface import Timeline_Repo_Interface
from database import execute_db, get_user_id, query_db

class Timeline_Repo(Timeline_Repo_Interface):
    def get_user_timeline(self, user_id, per_page_limit):
        return query_db('''
                select messages.*, users.* from messages, users
                where messages.flagged = 0 and messages.author_id = users.user_id and (
                    users.user_id = %s or
                    users.user_id in (select whom_id from followers
                                            where who_id = %s))
                order by messages.pub_date desc limit %s''',
                [user_id, user_id, per_page_limit])
    
    def get_public_timeline(self, per_page_limit):
        return query_db('''select messages.*, users.* from messages, users
          where messages.flagged = 0 and messages.author_id = users.user_id
            order by messages.pub_date desc limit %s''', [per_page_limit])
    
    def get_follower_timeline(self,username, per_page_limit):
        user_id = get_user_id(username)

        if user_id is None:
            return []
        
        return query_db('''
            select messages.*, users.* from messages, users where
            users.user_id = messages.author_id and users.user_id = %s
            order by messages.pub_date desc limit %s''',
            [user_id, per_page_limit])
    