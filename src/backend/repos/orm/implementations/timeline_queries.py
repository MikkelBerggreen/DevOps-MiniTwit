from repos.interfaces.timeline_repo_interface import Timeline_Repo_Interface
from database.db_orm import Database

from repos.orm.implementations.models import Latest

database = Database()


class Timeline_Repo(Timeline_Repo_Interface):
    def get_user_timeline(self, user_id, per_page_limit):
        # To implement
        pass

    def get_public_timeline(self, per_page_limit):
        # To implement
        pass

    def get_follower_timeline(self, username, per_page_limit):
        # To implement
        pass

    def record_latest(self, latest):
        with database.connect_db() as db:
            db_latest = Latest(latest_id=latest)
            db.add(db_latest)
            db.commit()
            db.refresh(db_latest)
            return db_latest

    def get_latest(self):
        with database.connect_db() as db:
            latest = db.query(Latest).one().latest_id
            return latest