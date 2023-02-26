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


#There is a weird interaction. main_test.py must exist in order to import all necessary app functions.

class EndpointTest_Example(unittest.TestCase):

    # Example of service testing
    @patch.object(Database, 'query_db')
    def test_proof(self):
        assert True == True