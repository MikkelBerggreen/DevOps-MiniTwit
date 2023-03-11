from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repos.orm.implementations.models import Base
from sqlalchemy_utils import database_exists, create_database

url = "postgresql://postgres:postgres@localhost:5442/minitwit"
engine = create_engine(url)
if not database_exists(engine.url):
    create_database(engine.url)

# connection URL: 'postgresql://postgres:password@host:port/database'
# engine = create_engine('postgresql://postgres:postgres@host.docker.internal:5442/minitwit')


Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


class Database:

    @contextmanager
    def connect_db(self):
        db = Session()
        try:
            yield db
        finally:
            db.close()

