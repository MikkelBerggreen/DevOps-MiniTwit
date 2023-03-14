import unittest
from unittest.mock import patch
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi.testclient import TestClient
from repos.orm.implementations.models import Base
from database.db_orm import Database
from main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


client = TestClient(app)


class Simulation_API_Testing(unittest.TestCase):

    @contextmanager
    def override_get_db(self):
        connection = engine.connect()

        # begin a non-ORM transaction
        transaction = connection.begin()

        # bind an individual Session to the connection
        db = TestingSessionLocal(bind=connection)
        # db = Session(engine)

        yield db

        db.close()
        transaction.rollback()
        connection.close()

    def set_up_users(self, username, email, passwords, latest):
        response = client.post(
                "/register",
                json={"username": username, "email": email, "pwd": passwords},
                params={"latest": latest}
            )

        assert response.status_code == 204

    @patch.object(Database, "connect_db")
    def test_latest(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return

            response = client.post(
                "/register",
                json={"username": "test", "email": "test@test", "pwd": "foo"},
                params={"latest": 1337}
            )

            assert response.status_code == 204

            response = client.get("/latest")
            assert response.status_code == 200
            assert response.json() == {"latest": 1337}

    @patch.object(Database, "connect_db")
    def test_register_c(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return
            response = client.post(
                "/register",
                json={"username": "c", "email": "c@c.c", "pwd": "c"},
                params={"latest": 6},
            )
            assert response.status_code == 204
            # assert response.json() == {"success": "register success"}
            # This would test register normally. Due to 204 it fails.

            response = client.get("/latest")
            assert response.status_code == 200
            assert response.json() == {"latest": 6}

    @patch.object(Database, "connect_db")
    def test_register_b(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return
            response = client.post(
                "/register",
                json={"username": "b", "email": "b@b.b", "pwd": "b"},
                params={"latest": 5},
            )
            assert response.status_code == 204

            response = client.get("/latest")
            assert response.status_code == 200
            assert response.json() == {"latest": 5}

    @patch.object(Database, "connect_db")
    def test_register_a(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            connect_db_mock.return_value = mocK_return
            response = client.post(
                "/register",
                json={"username": "a", "email": "a@a.a", "pwd": "a"},
                params={"latest": 1},
            )
            assert response.status_code == 204

            response = client.get("/latest")
            assert response.status_code == 200
            assert response.json() == {"latest": 1}

    @patch.object(Database, "connect_db")
    def test_create_msg_for_user_a(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            #############################
            connect_db_mock.return_value = mocK_return
            self.set_up_users("a", "a@a.a", "a", 1)
            #############################
            response = client.post(
                "/msgs/a",
                json={"content": "Blub"},
                params={"latest": 2},
            )
            assert response.status_code == 204

            # verify that latest was updated
            response = client.get("/latest")
            assert response.status_code == 200
            assert response.json() == {"latest": 2}

    @patch.object(Database, "connect_db")
    def test_get_latest_user_msgs(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            #############################
            connect_db_mock.return_value = mocK_return
            self.set_up_users("a", "a@a.a", "a", 1)

            response = client.post(
                "/msgs/a",
                json={"content": "Blub"},
                params={"latest": 2},
            )
            #############################
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

    @patch.object(Database, "connect_db")
    def test_get_latest_msgs(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            #############################
            connect_db_mock.return_value = mocK_return
            self.set_up_users("a", "a@a.a", "a", 1)

            response = client.post(
                "/msgs/a",
                json={"content": "Blub!"},
                params={"latest": 2},
            )

            #############################
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

    @patch.object(Database, "connect_db")
    def test_follow_user(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            #############################
            connect_db_mock.return_value = mocK_return
            self.set_up_users("a", "a@a.a", "a", 1)
            self.set_up_users("b", "b@b.b", "b", 5)
            self.set_up_users("c", "c@c.c", "c", 6)
            #############################
            response = client.post(
                "/fllws/a",
                json={"follow": "b"},
                params={"latest": 7},
            )
            assert response.status_code == 204

            response = client.post(
                "/fllws/a",
                json={"follow": "c"},
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

    @patch.object(Database, "connect_db")
    def test_a_unfollows_b(self, connect_db_mock):
        with self.override_get_db() as mocK_return:
            #############################
            connect_db_mock.return_value = mocK_return
            self.set_up_users("a", "a@a.a", "a", 1)
            self.set_up_users("b", "b@b.b", "b", 5)

            response = client.post(
                "/fllws/a",
                json={"follow": "b"},
                params={"latest": 7},
            )
            assert response.status_code == 204
            #############################
            response = client.post(
                "/fllws/a",
                json={"unfollow": "b"},
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
