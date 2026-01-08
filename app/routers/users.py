import time
from fastapi import APIRouter, Depends, HTTPException

from app.utils.db import get_session
from app.cruds.users import user_crud
from app.schemas.users import UserLogin
from app.schemas.users import UserCreate
from app.utils.jwt import Hash
from app.utils.password import check_password, hash_password

router = APIRouter()


@router.get("/{user_id}")
async def get_user(user_id: int, db=Depends(get_session)):
    """
    Get user by ID.
    """
    result = await user_crud.get(user_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.get("/")
async def get_all_users(db=Depends(get_session)):
    """
    Get all users.
    """
    result = await user_crud.all(db)
    return result


@router.post("/login")
async def login(user: UserLogin, db=Depends(get_session)):
    """
    User login.
    """
    res = await user_crud.get_by_username(user.username, db)
    if not res:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not check_password(user.password, res.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token, refresh_token = Hash.create_tokens({"user_id": res.id})
    return {"message": "Login successful", "user": user.username, "access_token": access_token, "refresh_token": refresh_token}


@router.post("/register")
async def register(user: UserLogin, db=Depends(get_session)):
    """
    User registration.
    """
    res = await user_crud.get_by_username(user.username, db)
    if res:
        raise HTTPException(status_code=400, detail="Username already exists")
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if len(user.password) < 6:
        raise HTTPException(
            status_code=400, detail="Password must be at least 6 characters long")
    if len(user.username) < 3:
        raise HTTPException(
            status_code=400, detail="Username must be at least 3 characters long")
    user_data = UserCreate(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    user = await user_crud.create(user_data, db)
    access_token, refresh_token = Hash.create_tokens({"user_id": user.id})
    return {"message": "User created successfully", "user": user.username, "access_token": access_token, "refresh_token": refresh_token}


# @router.get("/test/")
# async def get_test():
#     """
#     Get all users.
#     """
#     return [{"id": 1, "username": "test1"}, {"id": 2, "username": "test2"}]
