from repos.interfaces.timeline_repo_interface import Timeline_Repo_Interface
from database.db_orm import Database

from repos.orm.implementations.models import Latest, Message, User, Follower

from repos.orm.implementations.user_queries import User_Repo
database = Database()
user_repo = User_Repo()


class Timeline_Repo(Timeline_Repo_Interface):
    def get_user_timeline(self, user_id, per_page_limit, page):
        offset = (page * per_page_limit) - per_page_limit
        with database.connect_db() as db:
            follower = self.follow_dict(db.query(Follower).filter_by(who_id=user_id).all())

            following_ids = [followee["whom_id"] for followee in follower]

            query = db.query(Message, User).join(User, User.user_id == Message.author_id)\
                .filter(Message.flagged == 0)\
                .filter((User.user_id == user_id) | (User.user_id.in_(following_ids)))\
                .order_by(Message.pub_date.desc()).offset(offset)\
                .limit(per_page_limit).all()

            results = self.object_as_dict(query)

            return results

    def get_public_timeline(self, per_page_limit, page):
        offset = (page * per_page_limit) - per_page_limit
        with database.connect_db() as db:
            followers = db.query(Message, User)\
                .join(User, User.user_id == Message.author_id)\
                .where(Message.flagged == 0)\
                .order_by(Message.pub_date.desc()).offset(offset)\
                .limit(per_page_limit).all()
            return self.object_as_dict(followers)

    def get_follower_timeline(self, username, per_page_limit, page):
        user_id = user_repo.get_user_id_from_username(username)

        if user_id is None:
            return []
        offset = (page * per_page_limit) - per_page_limit

        with database.connect_db() as db:
            followers = db.query(Message, User)\
                .join(User, User.user_id == Message.author_id)\
                .where(User.user_id == user_id)\
                .order_by(Message.pub_date.desc()).offset(offset)\
                .limit(per_page_limit).all()
            return self.object_as_dict(followers)

    def record_latest(self, latest):
        with database.connect_db() as db:
            db_latest = Latest(latest_id=latest)
            db.add(db_latest)
            db.commit()
            db.refresh(db_latest)
            return db_latest

    def get_latest(self):
        with database.connect_db() as db:
            latest = db.query(Latest).order_by(Latest.id.desc()).first().latest_id
            return latest

    def object_as_dict(self, obj):
        dict_list = []
        for row in obj:
            dict_list.append({**row.User.__dict__, **row.Message.__dict__})
        return dict_list

    def follow_dict(self, obj):
        dict_list = []
        for row in obj:
            dict_list.append(row.__dict__)
        return dict_list
