from .base import RepositoryBase
from app.database.models.realm import Realm
from app.schemas.realm import RealmCreate, RealmUpdate


class RealmRepository(RepositoryBase[Realm, RealmCreate, RealmUpdate]):
    pass


realm_repository = RealmRepository(Realm)
