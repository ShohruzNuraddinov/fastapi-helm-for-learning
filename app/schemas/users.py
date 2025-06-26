from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base model for User.
    """
    username: str


class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    username: str
    email: str = None
    hashed_password: str


class UserUpdate(UserBase):
    """
    Model for updating an existing user.
    """
    id: int
    username: str = None
    password: str = None


class UserLogin(UserBase):
    """
    Model for user login.
    """
    username: str
    email: str = None
    password: str
