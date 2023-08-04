from typing import Any, Generator, Dict
from fastapi import Depends, HTTPException

from app.database.db import SessionLocal


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session
