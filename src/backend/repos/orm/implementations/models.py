from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    pw_hash = Column(String, nullable=False)

    messages = relationship('Message', backref='author')
    followers = relationship("Follower", foreign_keys="[Follower.who_id]", back_populates="who")
    following = relationship("Follower", foreign_keys="[Follower.whom_id]", back_populates="whom")

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Follower(Base):
    __tablename__ = 'followers'

    who_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    whom_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    who = relationship("User", foreign_keys=[who_id], back_populates="followers")
    whom = relationship("User", foreign_keys=[whom_id], back_populates="following")

    def __init__(self, who_id, whom_id):
        self.who_id = who_id
        self.whom_id = whom_id

    def __repr__(self):
        return f"Follower('{self.who_id}', '{self.whom_id}')"


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    text = Column(String, nullable=False)
    pub_date = Column(Integer, nullable=True)
    flagged = Column(Integer, nullable=True)

    def __init__(self, author_id, text, pub_date, flagged):
        self.author_id = author_id
        self.text = text
        self.pub_date = pub_date
        self.flagged = flagged

    def __repr__(self):
        return f"Message('{self.author_id}', '{self.text}', '{self.pub_date}', '{self.flagged}')"


class Latest(Base):
    __tablename__ = 'latest'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latest_id = Column(Integer)

    def __init__(self, latest_id):
        self.latest_id = latest_id

    def __repr__(self):
        return f"Latest('{self.latest_id}')"
