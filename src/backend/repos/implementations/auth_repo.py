from database.db_util import Database
from repos.interfaces.auth_repo_interface import Auth_Repo_Interface

database = Database()


class Auth_Repo(Auth_Repo_Interface):
    def check_if_user_exists(self, username):
        user = database.query_db(
            """SELECT * FROM users WHERE username = %s""", [username], one=True
        )
        if user is None:
            return False
        return True

    def validate_user(self, username, password):
        user = database.query_db(
            """SELECT * FROM users WHERE username = %s""", [username], one=True
        )
        if user is None or not password == user["pw_hash"]:
            return None
        return user

    def register_user(self, username, email, password):
        database.insert_in_db(
            """INSERT INTO users(username, email, pw_hash) VALUES(%s, %s, %s); """,
            [username, email, password],
        )
