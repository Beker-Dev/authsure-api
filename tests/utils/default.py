from app.repository.user import user_repository
from app.schemas.user import UserCreate
from app.repository.realm import realm_repository
from app.schemas.realm import RealmCreate


def create_default_user(db):
    realm = create_default_realm(db)

    return user_repository.create(
        db,
        UserCreate(
            username="admin",
            password="admin.admin",
            email="admin@email.com",
            realm_id=realm.id
        )
    )


def create_default_realm(db):
    return realm_repository.create(db, RealmCreate(name="default"))
