from datetime import timedelta, datetime
from enum import Enum

from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    """Everything related to hashing including jwt and passwords"""

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)

    @staticmethod
    def create_tokens(data: dict):
        access_token_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token_data = data.copy()
        access_token_data.update({
            "exp": access_token_expire,
            "token_type": "access"
        })

        refresh_token_data = data.copy()
        refresh_token_data.update({
            "exp": refresh_token_expire,
            "token_type": "refresh"
        })

        access_token = jwt.encode(access_token_data, SECRET_KEY, ALGORITHM)
        refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, ALGORITHM)

        return access_token, refresh_token

    @staticmethod
    def verify_token_access(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            token_type = payload.get("token_type")

            if not token_type or token_type != "access":
                raise HTTPException(status_code=401, detail={"detail": "Invalid access token",
                                                             "code": "invalid_access_token"
                                                             })

            id: str = payload.get("user_id")

            if id is None:
                raise credentials_exception

        except (JWTError, ExpiredSignatureError):
            raise credentials_exception
        return id

    @staticmethod
    def refresh_access_token(refresh_token):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            token_type = payload.get("token_type")

            if not token_type or token_type != "refresh":
                raise HTTPException(status_code=401, detail={"detail": "Invalid refresh token",
                                                             "code": "invalid_refresh_token"
                                                             })

            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail={"detail": "Invalid credentials",
                                                             "code": "invalid_credentials"
                                                             })

            new_access_token, refresh_token = Hash.create_tokens(data={"user_id": user_id})
            return new_access_token, refresh_token
        except (JWTError, ExpiredSignatureError):
            raise HTTPException(status_code=401,
                                detail={'detail': 'Invalid refresh token', 'code': 'invalid_refresh_token'})
