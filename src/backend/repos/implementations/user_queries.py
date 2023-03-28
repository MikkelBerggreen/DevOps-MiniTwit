from repos.interfaces.user_repo_interface import User_Repo_Interface
from database.models import User, Follower, Message
from database.db_orm import Database
import time
database = Database()


class User_Repo(User_Repo_Interface):
    def post_message(self, user_id, message):
        with database.connect_db() as db:
            message = Message(author_id=user_id, text=message, pub_date=int(time.time()), flagged=0)
            db.add(message)
            db.commit()
            db.refresh(message)
            return message

    def remove_follower(self, user_id, follower_id):
        with database.connect_db() as db:
            db.query(Follower).filter_by(who_id=user_id, whom_id=follower_id).delete()
            db.commit()

    def add_follower(self, user_id, follower_id):
        with database.connect_db() as db:
            follower_db = Follower(who_id=user_id, whom_id=follower_id)
            db.add(follower_db)
            db.commit()
            db.refresh(follower_db)
            return follower_db

    def get_all_followers(self, user_id, limit):
        with database.connect_db() as db:
            followers = db.query(User).join(Follower, User.user_id == Follower.whom_id).where(Follower.who_id == user_id).limit(limit).all()
            return followers

    def get_user_id_from_username(self, username):
        with database.connect_db() as db:
            user = db.query(User).filter_by(username=username).one_or_none()
            if user:
                return user.user_id
            else:
                return None

    def check_if_following(self, user_id, follower_id):
        with database.connect_db() as db:
            user = db.query(Follower).filter_by(who_id=user_id, whom_id=follower_id).one_or_none()
            if user is not None:
                return True
            else:
                return False
