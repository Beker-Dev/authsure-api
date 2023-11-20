from fastapi import HTTPException

from tests.utils.base import TestBase
from app.schemas.role import RoleCreate, RoleShow
from app.repository.role import role_repository
from app.core.config import settings


class TestRole(TestBase):
    url: str = "/api/roles"
    url_query: str = f"/api/roles?realm={settings.DEFAULT_REALM_NAME}"

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_show_roles(self):
        response = self.client.get(self.url_query, headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
