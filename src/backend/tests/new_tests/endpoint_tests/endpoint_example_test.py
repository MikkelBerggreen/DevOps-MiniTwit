import unittest
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app
from database.db_util import Database

from services.implementions.auth_service import Auth_Service

client = TestClient(app)


# Example of param testing testing
@pytest.mark.parametrize("count,expected",
                         [(0, 0), (1, 1), (25, 25), (0, 0)]
                         )
def test_param_example(count, expected):
    assert count == expected


class Second_Test(unittest.TestCase):

    def test_example(self):
        assert True == True