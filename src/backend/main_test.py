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
    
    # Example of template testing
    @patch.object(Database, 'query_db')
    @patch.object(Database, 'insert_in_db')
    @patch.object(Database, 'get_user_id')
    @patch.object(Database, 'execute_db')
    def test_testing_login(self, Execute_Mock, Get_ID_mock, Insert_Mock, Query_DB_Mock):
        mock_Return = {'user_id': 2, 'username': 'Test', 'email': 'Test', 'pw_hash': '0cbc6611f5540bd0809a388dc95a615b'}
        Query_DB_Mock.side_effect = [mock_Return, []]

        Insert_Mock.return_value = None

        Get_ID_mock.return_value = None

        Execute_Mock.return_value = None

        response = client.post(
            "/api/auth/login/",
            data={"username": "Test", "password": "Test"},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert 'sign out [Test]' in response.text

    # Example of service testing
    @patch.object(Database, 'query_db')
    def test_login_service(self, Query_DB_Mock):
        mock_Return = {'user_id': 2, 'username': 'Test', 'email': 'Test', 'pw_hash': '0cbc6611f5540bd0809a388dc95a615b'}
        Query_DB_Mock.return_value = mock_Return

        result = Auth_Service().validate_user("Test", "Test")
        assert result == mock_Return