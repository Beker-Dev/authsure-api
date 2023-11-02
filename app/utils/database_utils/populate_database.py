from sqlalchemy.orm import Session
from faker import Faker
import random
import string

from app.database.models.base import Base
from app.database.db import engine
from app.repository.user import user_repository
from app.repository.session import session_repository
from app.repository.role import role_repository
from app.repository.group import group_repository
from app.repository.client import client_repository
from app.repository.realm import realm_repository
from app.schemas.user import UserCreate
from app.schemas.session import SessionCreate
from app.schemas.role import RoleCreate
from app.schemas.group import GroupCreate
from app.schemas.client import ClientCreate
from app.schemas.realm import RealmCreate


class PopulateDatabase:
    def __init__(self, db_session: Session, items_per_model: int = 5):
        self.db_session = db_session
        self.faker = Faker(locale='PT-BR')
        self.items_per_model = items_per_model
        self.users = list()
        self.sessions = list()
        self.roles = list()
        self.groups = list()
        self.clients = list()
        self.realms = list()

    def __reset_database(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def __populate_users(self):
        for _ in range(self.items_per_model):
            user = UserCreate(
                username=self.faker.user_name(),
                email=self.faker.email(),
                password=self.faker.password(),
                realm_id=random.choice(self.realms).id
            )
            self.users.append(
                user_repository.create(self.db_session, obj_in=user)
            )

    def __populate_sessions(self):
        for _ in range(self.items_per_model):
            token = 'ey' + ''.join(random.choices(string.ascii_letters + string.digits + '.', k=64))
            session = SessionCreate(
                token=token,
                is_active=self.faker.pybool(),
                user_id=random.choice(self.users).id
            )
            self.sessions.append(
                session_repository.create(self.db_session, obj_in=session)
            )

    def __populate_roles(self):
        for _ in range(self.items_per_model):
            role = RoleCreate(
                name=self.faker.name(),
            )
            self.roles.append(
                role_repository.create(self.db_session, obj_in=role)
            )

    def __populate_groups(self):
        for _ in range(self.items_per_model):
            group = GroupCreate(
                name=self.faker.name(),
            )
            self.groups.append(
                group_repository.create(self.db_session, obj_in=group)
            )

    def __populate_clients(self):
        for _ in range(self.items_per_model):
            client = ClientCreate(
                name=self.faker.name(),
                description=self.faker.text(),
                key=self.faker.name(),
                secret=self.faker.password(),
                realm_id=random.choice(self.realms).id
            )
            self.clients.append(
                client_repository.create(self.db_session, obj_in=client)
            )

    def __populate_realms(self):
        for _ in range(self.items_per_model):
            realm = RealmCreate(name=self.faker.name())
            self.realms.append(
                realm_repository.create(self.db_session, obj_in=realm)
            )

    def __populate_user_admin(self):
        user = UserCreate(
            username="admin",
            email="admin.admin@email.com",
            password="admin",
            realm_id=random.choice(self.realms).id
        )
        self.users.append(
            user_repository.create(self.db_session, obj_in=user)
        )

    def populate(self, reset: bool = False):
        self.__reset_database() if reset else ...

        methods = [
            self.__populate_realms,
            self.__populate_clients,
            self.__populate_roles,
            self.__populate_groups,
            self.__populate_users,
            self.__populate_user_admin,
            self.__populate_sessions,
        ]

        [m() for m in methods]
