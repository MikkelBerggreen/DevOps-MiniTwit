import unittest

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Example of param testing
@pytest.mark.parametrize("count,expected", [(0, 0), (1, 1), (25, 25), (0, 0)])
def test_param_example(count, expected):
    assert count == expected


class Second_Test(unittest.TestCase):

    # Note parametrize testing does not work inside a unittest class.
    # This class is used to illustrate this.
    def test_example(self):
        assert True is True
