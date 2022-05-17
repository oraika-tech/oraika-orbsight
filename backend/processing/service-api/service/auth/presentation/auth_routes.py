from typing import Any

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from .model.response import Token, UserInfoResponse

from service.common.deps import create_access_token, get_current_user, get_auth_handler

routes = APIRouter()


@routes.post("/login", response_model=Token)
def login_access_token(
        response: Response, handler=Depends(get_auth_handler), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user_id = handler.verify_user(form_data.username, form_data.password)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect login_name or password")

    return Token(access_token=create_access_token(user_id), token_type="bearer")


@routes.get("/user/me", response_model=UserInfoResponse)
def current_user_info(user_info=Depends(get_current_user)) -> Any:
    if not user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    return UserInfoResponse(name=user_info.name)
