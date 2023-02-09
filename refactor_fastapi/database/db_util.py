import sqlite3
from contextlib import closing


def connect_db(DATABASE_URL):
    """Returns a new connection to the database."""
    print(DATABASE_URL)
    return sqlite3.connect(DATABASE_URL)


def init_db():
    """Creates the database tables."""
    pass
"""     with closing(connect_db()) as db:
        with app.open_resource('schema.sql', 'r') as f:
            db.cursor().executescript(f.read())
        db.commit() """
    
