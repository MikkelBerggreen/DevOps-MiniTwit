from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, aliased, joinedload
from orm.implementations.models import Base, User, Message, Follower

# connection URL: 'postgresql://postgres:password@host:port/database'
#engine = create_engine('postgresql://postgres:postgres@host.docker.internal:5442/minitwit')
engine = create_engine('postgresql://postgres:postgres@localhost:5442/minitwit')


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

class Timeline_Queries():
    def get_user_timeline(self, user_id, per_page_limit):
        user = session.query(User).filter_by(user_id=user_id).one()
        following_ids = [follower.whom_id for follower in user.following]

        query = session.query(Message, User).join(User)\
                      .filter(Message.flagged == 0)\
                      .filter((User.user_id == user_id) | (User.user_id.in_(following_ids)))\
                      .order_by(Message.pub_date.desc())\
                      .limit(per_page_limit)\
                      .options(
                          # Load the author relationship to avoid additional queries
                          joinedload(Message.author)
                      )

        results = query.all()

        return results