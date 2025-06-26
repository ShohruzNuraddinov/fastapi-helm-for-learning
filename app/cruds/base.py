from typing import Generic, Optional, TypeVar, Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from sqlmodel import SQLModel, select
from pydantic import BaseModel

from app.utils.db import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD class for SQLModel models.
    """
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, id: int, db_session: Optional[AsyncSession] = None) -> Optional[ModelType]:
        db_session = db_session or Depends(get_session)
        query = select(self.model).where(self.model.id == id)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()

    async def all(self, db_session: Optional[AsyncSession]) -> list[ModelType]:
        db_session = db_session or Depends(get_session)
        query = select(self.model)
        result = await db_session.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: CreateSchemaType, db_session: AsyncSession) -> ModelType:
        obj = self.model.from_orm(obj_in)
        try:
            db_session.add(obj)
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            raise ValueError("Integrity error occurred while creating the object.")
        await db_session.refresh(obj)
        return obj

    async def update(self, obj_in: UpdateSchemaType, db_session: AsyncSession) -> ModelType:
        obj = await self.get(obj_in.id, db_session)
        if not obj:
            raise ValueError("Object not found.")
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        try:
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            raise ValueError("Integrity error occurred while updating the object.")
        await db_session.refresh(obj)
        return obj


    async def delete(self, id: int, db_session: AsyncSession) -> Union[ModelType, None]:
        obj = await self.get(id, db_session)
        if not obj:
            raise ValueError("Object not found.")
        try:
            await db_session.delete(obj)
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            raise ValueError("Integrity error occurred while deleting the object.")
        return obj


