from repos.interfaces.user_repo_interface import User_Repo_Interface
from database import execute_db, get_user_id, query_db
import time

class User_Repo(User_Repo_Interface):
    def post_message(self, user_id, message):
        execute_db('''insert into messages (author_id, text, pub_date, flagged)
                values (?, ?, ?, 0)''', [user_id, message, int(time.time())])
        
    def remove_follower(self, user_id, follower_username):
        follower_id = get_user_id(follower_username)

        if follower_id is None:
            return False
        
        execute_db('delete from followers where who_id=? and whom_id=?',
               [user_id, follower_id])
        
        return True
    
    def add_follower(self, user_id, follower_username):
        follower_id = get_user_id(follower_username)

        if follower_id is None:
            return False
        
        execute_db('insert into followers (who_id, whom_id) values (?, ?)',
                [user_id, follower_id])
        
        return True
    
    def get_all_followers(self, user_id, limit):
        query = """SELECT user.username FROM user
                        WHERE follower.who_id=?
                        LIMIT ?"""
        return query_db(query, [user_id, limit])