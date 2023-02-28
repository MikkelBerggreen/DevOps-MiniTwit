from database.db_util import Database
from repos.interfaces.auth_repo_interface import Auth_Repo_Interface
import hashlib

database = Database()

class Auth_Repo(Auth_Repo_Interface):

    def check_if_user_exists(self, username):
        user = database.query_db('''SELECT * FROM users WHERE username = %s''', [username], one=True)
        if user is None:
            return False
        return True

    def validate_user(self, username, password):
        user = database.query_db('''SELECT * FROM users WHERE username = %s''', [username], one=True)
        hashed_pw = hashlib.md5(password.encode())
        if user is None or not hashed_pw.hexdigest() == user['pw_hash']:
            return None
        return user

    def register_user(self, username, email, password):
        hashed_pw = hashlib.md5(password.encode())
        database.insert_in_db('''INSERT INTO users(username, email, pw_hash) VALUES(%s, %s, %s); ''',
                     [username, email, hashed_pw.hexdigest()])

    def record_latest(self, latest):
        insert_in_db('''INSERT INTO latest(latest_id) VALUES(%s); ''',
                     [latest])

    
    def get_latest(self):
       return query_db('''select latest_id from latest order by id desc limit 1 ''', one=True).get('latest_id')