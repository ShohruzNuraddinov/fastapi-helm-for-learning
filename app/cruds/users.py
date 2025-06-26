from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.cruds.base import BaseCRUD


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    """
    CRUD operations for the User model.
    """

    async def get_by_username(self, username: str, db_session: Optional[AsyncSession] = None) -> Optional[User]:
        """
        Get a user by username.
        """
        query = select(self.model).where(self.model.username == username)
        result = await db_session.execute(query)
        return result.scalar_one_or_none()


user_crud = UserCRUD(User)
