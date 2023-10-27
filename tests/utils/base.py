from fastapi.testclient import TestClient
from unittest import TestCase
import json
import time

from app.main import app
from app.core.config import settings
from app.core.dependencies import get_db
from app.database.models.base import Base
from app.database.db import engine
from .default import create_default_user


class TestBase(TestCase):
    client = TestClient(app)
    db_instance = None
    default_user = None
    token = None

    def setUp(self):
        self.reset_database()
        self.db_instance = next(get_db())
        self.default_user = create_default_user(self.db_instance)
        self.token = self.client.post(
            '/api/auth/login',
            json={"username": self.default_user.username, "password": "admin.admin"}
        ).json()['access']

    def tearDown(self):
        self.db_instance.close()

    def serialize(self, model_show, data, exclude=None):
        _json = json.loads(model_show.from_orm(model_show.validate(data)).json())
        if exclude:
            for _key in exclude:
                _json.pop(_key)
        return _json

    def reset_database(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
