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

    def retrieve_user_by_username(self, username):
        user = database.query_db(
            """SELECT * FROM users WHERE username = %s""", [username], one=True
        )
        return user

    def register_user(self, username, email, password):
        database.insert_in_db(
            """INSERT INTO users(username, email, pw_hash) VALUES(%s, %s, %s); """,
            [username, email, password],
        )

    def change_user_password(self, password, user_id):
        database.update_in_db(
            """UPDATE users SET pw_hash = %s WHERE user_id = %s; """,
            [password, user_id],
        )
