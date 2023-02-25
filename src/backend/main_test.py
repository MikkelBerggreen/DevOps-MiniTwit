# -*- coding: utf-8 -*-
"""
    MiniTwit Tests
    ~~~~~~~~~~~~~~

    Tests the MiniTwit application.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import unittest
import tempfile
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from database.db_util import Database

from services.implementions.auth_service import Auth_Service

client = TestClient(app)


class MiniTwitTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.app = TestClient(app)

    # helper functions

    def register(self, username, password, password2=None, email=None):
        """Helper function to register a user"""
        if password2 is None:
            password2 = password
        if email is None:
            email = username + '@example.com'
        return self.app.post('/register', data={
            'username': username,
            'password': password,
            'password2': password2,
            'email': email,
        }, follow_redirects=True)

    def register_and_login(self, username, password):
        """Registers and logs in in one go"""
        self.register(username, password)
        return self.login(username, password)

    def logout(self):
        """Helper function to logout"""
        return self.app.get('/logout', follow_redirects=True)

    def add_message(self, text):
        """Records a message"""
        rv = self.app.post('/add_message', data={'text': text},
                           follow_redirects=True)
        assert rv.status_code == 200
        assert rv.json() == {"message": "Your message was recorded"}

    @patch.object(Database, 'query_db')
    @patch.object(Database, 'insert_in_db')
    @patch.object(Database, 'get_user_id')
    @patch.object(Database, 'execute_db')
    def test_BookingRepo_GetAll_ServiceGetsMockData(self, Execute_Mock, Get_ID_mock, Insert_Mock, Query_DB_Mock):
        mock_Return = {'user_id': 2, 'username': 'Test', 'email': 'Test', 'pw_hash': '0cbc6611f5540bd0809a388dc95a615b'}
        Query_DB_Mock.side_effect = [mock_Return, []]

        Insert_Mock.return_value = None

        Get_ID_mock.return_value = None

        Execute_Mock.return_value = None

        response = client.post(
            "/api/auth/login/",
            data={"username": "Test", "password": "Test"},
            allow_redirects = True
        )
        assert response.status_code == 200
        assert 'sign out [Test]' in response.text

    # testing functions
    @unittest.skip("No way to test it just yet")
    def test_register(self):
        """Make sure registering works"""
        rv = self.register('user1', 'default')
        assert rv.status_code == 200
        assert rv.json() == {"message": "You were successfully registered and can login now"}
        rv = self.register('user1', 'default')
        assert rv.status_code == 400
        assert rv.json() == {"message": "The username is already taken"}
        rv = self.register('', 'default')
        assert rv.status_code == 400
        assert rv.json() == {"message": "You have to enter a username"}
        rv = self.register('meh', '')
        assert rv.status_code == 400
        assert rv.json() == {"message": "You have to enter a password"}
        rv = self.register('meh', 'x', 'y')
        assert rv.status_code == 400
        assert rv.json() == {"message": "The two passwords do not match"}
        rv = self.register('meh', 'foo', email='broken')
        assert rv.status_code == 400
        assert rv.json() == {"message": "You have to enter a valid email address"}

    @unittest.skip("No way to test it just yet")
    def test_login_logout(self):
        """Make sure logging in and logging out works"""
        rv = self.register_and_login('user1', 'default')
        assert rv.status_code == 200
        assert rv.json() == {"message": "You were logged in"}
        rv = self.logout()
        assert rv.status_code == 200
        assert rv.json() == {"message": "You were logged out"}
        rv = self.login('user1', 'wrongpassword')
        assert rv.status_code == 400
        assert rv.json() == {"message": "Invalid password"}
        rv = self.login('user2', 'wrongpassword')
        assert rv.status_code == 400
        assert rv.json() == {"message": "Invalid username"}

    @unittest.skip("No way to test it just yet")
    def test_message_recording(self):
        """Check if adding messages works"""
        self.register_and_login('foo', 'default')
        self.add_message('test message 1')
        self.add_message('<test message 2>')

    # This might need a total rewrite. Likely it is best to test the database and get all method
    @unittest.skip("No way to test it just yet")
    def test_timelines(self):
        """Make sure that timelines work"""
        self.register_and_login('foo', 'default')
        self.add_message('the message by foo')
        self.logout()
        self.register_and_login('bar', 'default')
        self.add_message('the message by bar')
        rv = self.app.get('/public')
        assert b'the message by foo' in rv.read()
        assert b'the message by bar' in rv.read()

        # bar's timeline should just show bar's message
        rv = self.app.get('/')
        assert b'the message by foo' not in rv.read()
        assert b'the message by bar' in rv.read()

        # now let's follow foo
        rv = self.app.get('/foo/follow', follow_redirects=True)
        assert b'You are now following &#34;foo&#34;' in rv.read()

        # we should now see foo's message
        rv = self.app.get('/')
        assert b'the message by foo' in rv.read()
        assert b'the message by bar' in rv.read()

        # but on the user's page we only want the user's message
        rv = self.app.get('/bar')
        assert b'the message by foo' not in rv.read()
        assert b'the message by bar' in rv.read()
        rv = self.app.get('/foo')
        assert b'the message by foo' in rv.read()
        assert b'the message by bar' not in rv.read()

        # now unfollow and check if that worked
        rv = self.app.get('/foo/unfollow', follow_redirects=True)
        assert b'You are no longer following &#34;foo&#34;' in rv.read()
        rv = self.app.get('/')
        assert b'the message by foo' not in rv.read()
        assert b'the message by bar' in rv.read()
