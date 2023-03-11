# -*- coding: utf-8 -*-
"""
    MiniTwit Tests
    ~~~~~~~~~~~~~~

    Tests the MiniTwit application.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from database.db_util import Database

from services.implementions.auth_service import Auth_Service

import bcrypt
import json

client = TestClient(app)


class MiniTwitTestCase(unittest.TestCase):

    @unittest.skip("No way to test it just yet")
    @patch.object(Database, "query_db")
    @patch.object(Database, "insert_in_db")
    def test_register_one_user(self, Insert_Mock, Query_DB_Mock):
        plain_password = ";;æøåÆØÅ!# truncate users;"
        mock_Return = {
            "user_id": 1,
            "username": "TestUser",
            "email": "test@email.com",
        }

        response = client.post(
            "/api/auth/register/",
            data={"username": "Test", "password": plain_password},
            allow_redirects=True,
        )
        assert response.status_code == 200

    @unittest.skip("No way to test it just yet")
    @patch.object(Database, "query_db")
    def test_cant_register_two_of_same_users(self, Query_DB_Mock):
        plain_password = ";;æøåÆØÅ!# truncate users;"
        mock_Return_user_one = {
            "user_id": 1,
            "username": "TestUser",
            "email": "test@email.com"
        }
        Query_DB_Mock.return_value = mock_Return_user_one
        mock_Return_user_two = {
            "username": "TestUser",
            "email": "test@email.com"
        }

        response_one = client.post(
            "/api/auth/register/",
            data=mock_Return_user_one,
            allow_redirects=True,
        )
        Query_DB_Mock.return_value = None

        assert response_one.status_code == 200

        response_two = client.post(
            "/api/auth/register/",
            data=mock_Return_user_two,
            # Note that in this test we are not allowing redirects
            allow_redirects=False,
        )
        assert response_two.status_code == 307


    @unittest.skip("No way to test it just yet")
    @patch.object(Database, "query_db")
    @patch.object(Database, "insert_in_db")
    @patch.object(Database, "get_user_id")
    @patch.object(Database, "execute_db")
    def test_testing_login(self, Execute_Mock, Get_ID_mock, Insert_Mock, Query_DB_Mock):
        plain_password = ";;æøåÆØÅ!# truncate users;'"
        encrypted_password = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        encrypted_password_decoded = encrypted_password.decode("utf8")
        mock_Return = {
            "user_id": 2,
            "username": "Test",
            "email": "Test@test.com",
            "pw_hash": encrypted_password_decoded,
        }
        Query_DB_Mock.side_effect = [mock_Return, []]

        Insert_Mock.return_value = None

        Get_ID_mock.return_value = None

        Execute_Mock.return_value = None

        response = client.post(
            "/api/auth/login/",
            data={"username": "Test", "password": plain_password},
            allow_redirects=True,
        )
        assert response.status_code == 200
        assert "sign out [Test]" in response.text

    # Example of service testing
    @unittest.skip("No way to test it just yet")
    @patch.object(Database, "query_db")
    def test_login_service(self, Query_DB_Mock):
        plain_password = ";;æøåÆØÅ!# truncate users;"
        encrypted_password = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        encrypted_password_decoded = encrypted_password.decode("utf8")
        mock_Return = {
            "user_id": 2,
            "username": "TestUser",
            "email": "TestPassword",
            "pw_hash": encrypted_password_decoded,
        }
        Query_DB_Mock.return_value = mock_Return

        result = Auth_Service().validate_user("TestUser", plain_password)
        assert result == mock_Return
