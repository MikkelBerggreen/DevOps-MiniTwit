from repos.interfaces.user_repo_interface import User_Repo_Interface
import time
from database.db_util import Database

database = Database()


class User_Repo(User_Repo_Interface):
    def post_message(self, user_id, message):
        database.execute_db(
            """insert into messages (author_id, text, pub_date, flagged)
                values (%s, %s, %s, 0)""",
            [user_id, message, int(time.time())],
        )

    def remove_follower(self, user_id, follower_id):

        database.execute_db(
            "delete from followers where who_id=%s and whom_id=%s",
            [user_id, follower_id],
        )

        return True

    def add_follower(self, user_id, follower_id):

        database.execute_db(
            "insert into followers (who_id, whom_id) values (%s, %s)",
            [user_id, follower_id],
        )

        return True

    def get_all_followers(self, user_id, limit):
        query = """
        SELECT users.username FROM users
        INNER JOIN followers ON followers.whom_id=users.user_id
                        WHERE followers.who_id= %s
                        LIMIT %s"""
        return database.query_db(query, [user_id, limit])

    def get_user_id_from_username(self, username):
        return database.get_user_id(username)

    def check_if_following(self, user_id, follower_id):

        return (
            database.query_db(
                """select 1 from followers where
            followers.who_id = %s and followers.whom_id = %s""",
                [user_id, follower_id],
                one=True,
            )
            is not None
        )
