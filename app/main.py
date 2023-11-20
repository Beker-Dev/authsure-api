from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routes import router
from app.core.config import settings
from app.database.db import engine
from app.database.models.base import Base
from app.utils.database_utils.populate_database import PopulateDatabaseDefaultInstances

from app.utils.repository_utils.get_repository import get_repository_by_name


def assemble_database():
    Base.metadata.create_all(bind=engine)
    PopulateDatabaseDefaultInstances().populate()


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.ROOT_PATH)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # _app.add_middleware(BaseHTTPMiddleware, dispatch=Authentication())
    _app.include_router(router)
    assemble_database()
    return _app


app = get_application()
