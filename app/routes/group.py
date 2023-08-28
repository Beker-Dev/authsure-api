from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.group import group_repository
from app.schemas.group import GroupShow, GroupCreate, GroupUpdate


router = APIRouter(tags=['Groups'], prefix='/groups')
