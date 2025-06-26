from typing import Optional
from sqlmodel import Field
from app.models.base import BaseModel


class User(BaseModel, table=True):
    """
    User model for the database.
    """
    __tablename__ = "users"

    username: str = Field(index=True, unique=True, nullable=False)
    email: Optional[str] = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
