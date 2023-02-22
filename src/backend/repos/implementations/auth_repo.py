from repos.interfaces.auth_repo_interface import Auth_Repo_Interface
from database import query_db, insert_in_db
import hashlib

class Auth_Repo(Auth_Repo_Interface):

    def check_if_user_exists(self, username):
        user = query_db('''select * from users where username = ?''', [username], one=True)
        if user is None:
            return False
        return True

    def validate_user(self, username, password):
        user = query_db('''select * from users where username = ?''', [username], one=True)
        hashed_pw = hashlib.md5(password.encode())
        if user is None or not hashed_pw.hexdigest() == user['pw_hash']:
            return None
        return user

    def register_user(self, username, email, password):
        hashed_pw = hashlib.md5(password.encode())
        insert_in_db('''
            insert into users (username, email, pw_hash)
            values (?, ?, ?)''',
                     [username, email, hashed_pw.hexdigest()])
