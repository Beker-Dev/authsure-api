from fastapi.testclient import TestClient
from unittest import TestCase
import json
import time

from app.main import app
from app.core.config import settings
from app.core.dependencies import get_db
from app.database.models.base import Base
from app.database.db import engine


class TestBase(TestCase):
    client = TestClient(app)
    db_instance = None

    def setUp(self):
        self.reset_database()
        self.db_instance = next(get_db())

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
