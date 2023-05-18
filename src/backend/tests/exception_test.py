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

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


client = TestClient(app)


class Exception_Testing(unittest.TestCase):

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