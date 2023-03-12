# -*- coding: utf-8 -*-
"""
    MiniTwit Tests
    ~~~~~~~~~~~~~~

    Tests the MiniTwit application.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import unittest
import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from database.db_util import Database

from repos.orm.implementations.auth_queries import Auth_Repo

from util.custom_exceptions import Custom_Exception

import bcrypt
import json

client = TestClient(app)


#NOTE: Do not add tests to this class, add tests to /tests/ folder. This class is only examples of tests !
# For more examples related to testing on live db. See /tests/sim_api_test.py


# Example of param testing
@pytest.mark.parametrize("count,expected", [(0, 0), (1, 1), (25, 25), (0, 0)])
def test_param_example(count, expected):
    assert count == expected

class MiniTwitTestCase(unittest.TestCase):

    # Note parametrize testing does not work inside a unittest class.
    # This class is used to illustrate this.
    # To skip tests. Use : 
    #    @unittest.skip("No way to test it just yet") 
    def test_example(self):
        assert True is True

    # Example of service testing + mocking objects
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
