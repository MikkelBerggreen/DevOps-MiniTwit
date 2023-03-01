from repos.interfaces.timeline_repo_interface import Timeline_Repo_Interface
from database.db_util import Database

database = Database()


class Timeline_Repo(Timeline_Repo_Interface):
    def get_user_timeline(self, user_id, per_page_limit):
        return database.query_db(
            """
                select messages.*, users.* from messages, users
                where messages.flagged = 0 and messages.author_id = users.user_id and (
                    users.user_id = %s or
                    users.user_id in (select whom_id from followers
                                            where who_id = %s))
                order by messages.pub_date desc limit %s""",
            [user_id, user_id, per_page_limit],
        )

    def get_public_timeline(self, per_page_limit):
        return database.query_db(
            """select messages.*, users.* from messages, users
          where messages.flagged = 0 and messages.author_id = users.user_id
            order by messages.pub_date desc limit %s""",
            [per_page_limit],
        )

    def get_follower_timeline(self, username, per_page_limit):
        user_id = database.get_user_id(username)

        if user_id is None:
            return []

        return database.query_db(
            """
            select messages.*, users.* from messages, users where
            users.user_id = messages.author_id and users.user_id = %s
            order by messages.pub_date desc limit %s""",
            [user_id, per_page_limit],
        )

    def record_latest(self, latest):
        database.insert_in_db(
            """INSERT INTO latest(latest_id) VALUES(%s); """, [latest]
        )

    def get_latest(self):
        return database.query_db(
            """select latest_id from latest order by id desc limit 1 """, one=True
        ).get("latest_id")
