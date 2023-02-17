from contextlib import closing
import sqlite3
from dotenv import dotenv_values
# Docker runs this file from src. 
dotenv = dotenv_values("../.env")
# To run this file from /utils the pash should be: "../backend/.env"

def init_db():
    """Creates the database tables."""
    connection = sqlite3.connect("/tmp/minitwit.db")
    with open('/app/database/schema.sql', 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

init_db()
