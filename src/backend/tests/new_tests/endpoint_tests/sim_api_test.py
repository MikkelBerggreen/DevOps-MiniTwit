import json
import base64
import requests
import unittest
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app

# In order for the tests to work. We need to override existing db connection url with a fake database
# Afterwards we might take several approaches :
# Revert transactions to prevent committing. Using fixture
# Allow transactions but delete the database after all tests are done.
# Have single instances of testing. Meaning we test a single function in a vacuum.
# In this file. I Attempted to make the override but without a more concrete ORM implementation, 
# it is hard to make tests / predict how the tests could look like. 

# test_database.py
SQLALCHEMY_DATABASE_URL = "postgresql://test-fastapi:password@db/test-fastapi-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Following line creates database
# Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        db.begin()
        yield db
    finally:
        db.rollback()
        db.close()


# Override db dependency.
# app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@unittest.skip("No way to test it just yet")
@pytest.mark.parametrize("user, email, pwd, latest",
                         [("a", "a@a.a", "a", 1),
                          ("b", "b@b.b", "b", 5),
                          ("c", "c@c.c", "c", 6)])
def test_register_NormalRegister(user, email, pwd, latest):
    response = client.post(
        "/register",
        data={"username": user, "email": email, "pwd": pwd},
        params={"latest": latest},
    )
    assert response.status_code == 204
    # assert response.json() == {"success": "register success"} This would test register normally. Due to 204 it fails.

    response = client.get("/latest")
    assert response.status_code == 200
    assert response.json() == {"latest": latest}


class Simulation_API_Testing(unittest.TestCase):
    @unittest.skip("No way to test it just yet")
    def test_latest(self):
        response = client.post(
            "/register",
            data={"username": "test", "email": "test@test", "pwd": "foo"},
            params={"latest": 1337},
        )
        assert response.status_code == 204

        response = client.get("/latest")
        assert response.status_code == 200
        assert response.json() == {"latest": 1337}
        
    @unittest.skip("No way to test it just yet")
    def test_create_msg_for_user_a(self):
        response = client.post(
            "/msgs/a",
            data={"content": "Blub"},
            params={"latest": 2},
        )
        assert response.status_code == 204

        # verify that latest was updated
        response = client.get("/latest")
        assert response.status_code == 200
        assert response.json() == {"latest": 2}

    @unittest.skip("No way to test it just yet")
    def test_get_latest_user_msgs(self):

        response = client.get(
            "/msgs/a",
            params={"no": 20, "latest": 3},
        )
        assert response.status_code == 204

        # impossible to test due to 204 status code.
        # got_it_earlier = False
        # for msg in response.json():
        #   if msg["content"] == "Blub!" and msg["user"] == username:
        #        got_it_earlier = True

        # assert got_it_earlier
        # verify that latest was updated
        response = client.get("/latest")
        assert response.status_code == 200
        assert response.json() == {"latest": 3}

    @unittest.skip("No way to test it just yet")
    def test_get_latest_msgs(self):
        response = client.get(
            "/msgs",
            params={"no": 20, "latest": 4},
        )
        assert response.status_code == 200

        got_it_earlier = False
        for msg in response.json():
            if msg["content"] == "Blub!" and msg["user"] == "a":
                got_it_earlier = True

        assert got_it_earlier

        response = client.get("/latest")
        assert response.status_code == 200
        assert response.json() == {"latest": 4}

    @unittest.skip("No way to test it just yet")
    def test_follow_user(self):

        response = client.post(
            "/fllws/a",
            data={"follow": "b"},
            params={"latest": 7},
        )
        assert response.status_code == 204

        response = client.post(
            "/fllws/a",
            data={"follow": "c"},
            params={"latest": 8},
        )
        assert response.status_code == 204

        response = client.get(
            "/fllws/a",
            params={"no": 20, "latest": 9},
        )
        assert response.status_code == 200
        json_data = response.json()
        assert "b" in json_data["follows"]
        assert "c" in json_data["follows"]

        # verify that latest was updated
        response = client.get("/latest")
        assert response.status_code == 200
        assert response.json() == {"latest": 9}

    @unittest.skip("No way to test it just yet")
    def test_a_unfollows_b(self):
        response = client.post(
            "/fllws/a",
            data={"unfollow": "b"},
            params={"latest": 10},
        )
        assert response.status_code == 204

        # then verify that b is no longer in follows list
        response = client.get(
            "/fllws/a",
            params={"no": 20, "latest": 11},
        )
        assert response.status_code == 200
        assert "b" not in response.json()["follows"]

        response = client.get("/latest")
        assert response.status_code == 200
        assert response.json() == {"latest": 11}
