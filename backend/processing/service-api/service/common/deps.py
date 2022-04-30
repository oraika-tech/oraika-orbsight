from datetime import timedelta, datetime
from typing import Union, Any, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from service.common.settings import settings
from starlette import status
from starlette.exceptions import HTTPException
from service.auth import auth_handler
from .model.user import UserInfo


class TokenPayload(BaseModel):
    sub: Optional[int] = None


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token"
)


def get_auth_handler():
    return auth_handler


def create_access_token(subject: Union[str, int, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(reusable_oauth2), handler=Depends(get_auth_handler)) -> UserInfo:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_id = token_data.sub
    user_info = handler.user_info(user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info
