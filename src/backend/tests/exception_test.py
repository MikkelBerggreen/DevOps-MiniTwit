import unittest

from unittest.mock import patch
from fastapi.testclient import TestClient

from repos.orm.implementations.auth_queries import Auth_Repo

from services.implementions.auth_service import Auth_Service
from main import app

client = TestClient(app)


class Exception_Test(unittest.TestCase):

    @patch.object(Auth_Repo, "validate_user")
    def test_cant_register_two_of_same_users(self, Query_DB_Mock):

        mock_Return_user_one = {
            "user_id": 1,
            "username": "TestUser",
            "email": "test@email.com"
        }
        Query_DB_Mock.return_value = mock_Return_user_one
        try:
            Auth_Service().register_user("TestUser", "test@email.com",  ";;æøåÆØÅ!# truncate users;")
            assert False
        except:
            assert True
