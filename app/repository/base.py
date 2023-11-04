from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pydantic import BaseModel
import math

from app.database.models.base import Base
from app.utils.repository_utils.database_handler import handle_session
from app.utils.repository_utils.filters import Filter, FilterJoin


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @handle_session
    def get_by_join(
            self,
            db: Session,
            filters: List[Filter] = None,
            filters_join: List[FilterJoin] = None,
            order_by=None,
    ):
        query_filters = []

        if filters is not None:
            for filter in filters:
                filter_conditions = [
                    getattr(self.model, filter.key) == value for value in filter.values
                ]
                query_filters.append(or_(*filter_conditions))
        query_filters = and_(*query_filters)

        query = db.query(self.model)
        if filters_join is not None:
            for filter in filters_join:
                query = query.join(filter.class_, filter.class_attr == filter.join_attr)
                filter_conditions = (
                    [
                        getattr(filter.class_, filter.class_key) == value
                        for value in filter.values
                    ]
                    if filter.values
                    else []
                )
                query_filters = and_(query_filters, or_(*filter_conditions))

        return query.filter(query_filters).order_by(order_by).all()

    @handle_session
    def get_by(self, db: Session, filters: dict, all: bool = False) -> Optional[ModelType]:
        if all:
            return db.query(self.model).filter_by(**filters).all()
        return db.query(self.model).filter_by(**filters).first()

    @handle_session
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    @handle_session
    def get_or_404(self, db: Session, id: Any) -> Optional[ModelType]:
        db_query = db.query(self.model).filter(self.model.id == id).first()
        if not db_query:
            raise HTTPException(404, f"{self.model.__name__} not found")
        return db_query

    @handle_session
    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    @handle_session
    def get_count(self, db: Session) -> int:
        return db.query(self.model).count()

    @handle_session
    def get_last_page(self, db: Session, limit: int) -> int:
        results = db.query(self.model).count()
        return math.ceil(results / limit)

    @handle_session
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @handle_session
    def create_with_association(
        self, db: Session, obj_in: CreateSchemaType
    ) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @handle_session
    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = (
            obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        )

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @handle_session
    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
