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
import database

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class MiniTwitTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db = tempfile.NamedTemporaryFile()
        self.app = TestClient(app)
        app.DATABASE = self.db.name
        database.init_db()

    # helper functions

    def register(self, username, password, password2=None, email=None):
        """Helper function to register a user"""
        if password2 is None:
            password2 = password
        if email is None:
            email = username + '@example.com'
        return self.app.post('/register', data={
            'username':     username,
            'password':     password,
            'password2':    password2,
            'email':        email,
        }, follow_redirects=True)

    def login(self, username, password):
        """Helper function to login"""
        return self.app.post('/login', data={
            'username': username,
            'password': password
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
        if text:
            assert b'Your message was recorded' in rv.read()
        return rv

    # testing functions

    def test_register(self):
        """Make sure registering works"""
        rv = self.register('user1', 'default')
        assert b'You were successfully registered ' \
               b'and can login now' in rv.read()
        rv = self.register('user1', 'default')
        assert b'The username is already taken' in rv.read()
        rv = self.register('', 'default')
        assert b'You have to enter a username' in rv.read()
        rv = self.register('meh', '')
        assert b'You have to enter a password' in rv.read()
        rv = self.register('meh', 'x', 'y')
        assert b'The two passwords do not match' in rv.read()
        rv = self.register('meh', 'foo', email='broken')
        assert b'You have to enter a valid email address' in rv.read()

    def test_login_logout(self):
        """Make sure logging in and logging out works"""
        rv = self.register_and_login('user1', 'default')
        assert b'You were logged in' in rv.read()
        rv = self.logout()
        assert b'You were logged out' in rv.read()
        rv = self.login('user1', 'wrongpassword')
        assert b'Invalid password' in rv.read()
        rv = self.login('user2', 'wrongpassword')
        assert b'Invalid username' in rv.read()

    def test_message_recording(self):
        """Check if adding messages works"""
        self.register_and_login('foo', 'default')
        self.add_message('test message 1')
        self.add_message('<test message 2>')
        rv = self.app.get('/')
        assert b'test message 1' in rv.read()
        assert b'&lt;test message 2&gt;' in rv.read()

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


if __name__ == '__main__':
    unittest.main()
