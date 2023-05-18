import unittest
from unittest.mock import patch
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi.testclient import TestClient
from repos.orm.implementations.models import Base
from database.db_orm import Database
from main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@host.docker.internal:5432/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


client = TestClient(app)


class Old_Minitwit_GUI_Tests(unittest.TestCase):

    @contextmanager
    def override_get_db(self):
        connection = engine.connect()

        # begin a non-ORM transaction
        transaction = connection.begin()

        # bind an individual Session to the connection
        db = TestingSessionLocal(bind=connection)
        # db = Session(engine)

        yield db

        db.close()
        transaction.rollback()
        connection.close()

    # helper functions
    def register(self, username, password, password2=None, email=None):
        """Helper function to register a user"""
        if password2 is None:
            password2 = password
        if email is None:
            email = username + '@example.com'
        return client.post(
            "/api/auth/register",
            data={
                'username':     username,
                'password':     password,
                'password2':    password2,
                'email':        email,
            },
            allow_redirects=True,
        )

    def login(self, username, password):
        """Helper function to login"""
        return client.post(
            "/api/auth/login",
            data={
                'username':     username,
                'password':     password,
            },
            allow_redirects=True,
        )

    def register_and_login(self, username, password):
        """Registers and logs in in one go"""
        self.register(username, password)
        return self.login(username, password)

    def logout(self):
        """Helper function to logout"""
        return client.get('/logout', allow_redirects=True)

    def add_message(self, text):
        """Records a message"""
        return client.post(
                "/api/users/messages",
                data={"text": text},
                allow_redirects=True
            )

    # Clean up errors.
    def setUp(self):
        client.get('/logout', allow_redirects=True)

    # testing functions
    @patch.object(Database, "connect_db")
    def test_register(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return

            """Make sure registering works"""
            rv = self.register('user1', 'default')
            assert 'You are registered. You can now log in!' in rv.text
            rv = self.register('user1', 'default')
            assert 'User already exists' in rv.text
            rv = self.register('', 'default')
            assert 'Username cannot be blank' in rv.text
            rv = self.register('meh', '')
            assert 'Password cannot be blank' in rv.text
            rv = self.register('meh', 'x', 'y')
            assert 'The two passwords do not match' in rv.text
            rv = self.register('meh', 'foo', email='broken')
            assert 'You have to enter a valid email address' in rv.text

    @patch.object(Database, "connect_db")
    def test_login_logout(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return

            """Make sure logging in and logging out works"""
            rv = self.register_and_login('user1', 'default')
            assert 'You were logged in' in rv.text
            rv = self.logout()
            assert 'You were logged out' in rv.text
            rv = self.login('user1', 'wrongpassword')
            assert 'Password is Incorrect' in rv.text
            rv = self.login('user2', 'wrongpassword')
            assert 'username not found' in rv.text

    @patch.object(Database, "connect_db")
    def test_message_recording(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return

            """Check if adding messages works"""
            self.register_and_login('foo', 'default')
            self.add_message('test message 1')
            self.add_message('<test message 2>')
            rv = client.get('/')
            assert 'test message 1' in rv.text
            assert '&lt;test message 2&gt;' in rv.text

    @patch.object(Database, "connect_db")
    def test_timelines(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return

            """Make sure that timelines work"""
            self.register_and_login('foo', 'default')
            self.add_message('the message by foo')
            self.logout()
            self.register_and_login('bar', 'default')
            self.add_message('the message by bar')
            rv = client.get('/public')
            assert 'the message by foo' in rv.text
            assert 'the message by bar' in rv.text

            # bar's timeline should just show bar's message
            rv = client.get('/')
            assert 'the message by foo' not in rv.text
            assert 'the message by bar' in rv.text

            # now let's follow foo
            rv = client.get('/api/users/foo/follow', allow_redirects=True)
            assert 'You are now following &#34;foo&#34;' in rv.text

            # we should now see foo's message
            rv = client.get('/')
            assert 'the message by foo' in rv.text
            assert 'the message by bar' in rv.text

            # but on the user's page we only want the user's message
            rv = client.get('/timeline/bar')
            assert 'the message by foo' not in rv.text
            assert 'the message by bar' in rv.text
            rv = client.get('/timeline/foo')
            assert 'the message by foo' in rv.text
            assert 'the message by bar' not in rv.text

            # now unfollow and check if that worked
            rv = client.get('/api/users/foo/unfollow', allow_redirects=True)
            assert 'You are no longer following &#34;foo&#34;' in rv.text
            rv = client.get('/')
            assert 'the message by foo' not in rv.text
            assert 'the message by bar' in rv.text
