"""Token based auth"""

from string import digits
from random import sample
from datetime import datetime, timedelta
from functools import partial
from typing import Callable, Optional, Union  # , TYPE_CHECKING

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlmodel import Session, select

from division.config import settings
from division.database import engine
from division.models.constraints import RoleLevel
from division.utils.security import verify_password
from division.utils.session import get_session

from division.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


# Models


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Functions


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    scope: str = "access_token",
) -> str:
    """Creates a JWT Token from user data

    scope: access_token or refresh_token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "scope": scope})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,  # pyright: ignore
        algorithm=settings.ALGORITHM,  # pyright: ignore
    )
    return encoded_jwt


create_refresh_token = partial(create_access_token, scope="refresh_token")


def authenticate_user(get_user: Callable, username: str, password: str) -> Union[User, bool]:
    """Authenticate the user"""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user(username) -> Optional[User]:
    """Get user from database"""
    query = select(User).where(User.username == username)
    with Session(engine) as session:
        return session.exec(query).first()


def get_current_user(
    # pyright: ignore
    request: Request,
    token: str = Depends(oauth2_scheme),
    fresh=False,
) -> User:
    """Get current user authenticated"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if request:
        if session_id := request.cookies.get("session_id"):
            username = get_session(session_id)
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Session ID",
                )
            user = get_user(username=username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session user not found",
                )
            return user

        if authorization := request.headers.get("authorization"):
            try:
                token = authorization.split(" ")[1]
            except IndexError:
                raise credentials_exception

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            # pyright: ignore  # pyright: ignore
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str = payload.get("sub")  # pyright: ignore

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    if fresh and (not payload["fresh"] and not user.superuser):
        raise credentials_exception

    return user


# FastAPI dependencies


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Wraps the sync get_active_user for sync calls"""
    return current_user


AuthenticatedUser = Depends(get_current_active_user)


async def validate_token(token: str = Depends(oauth2_scheme)) -> User:
    """Validates user token"""
    user = get_current_user(token=token)
    return user


async def get_current_super_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role.level != RoleLevel.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a super user")
    return current_user


SuperUser = Depends(get_current_super_user)


async def get_current_user_or_none():
    """Returns the current user or None"""
    try:
        yield Depends(get_current_user)
    except HTTPException:
        yield None


async def get_user_if_change_password_is_allowed(
    *,
    request: Request,
    pwd_reset_token: Optional[str] = None,  # from path?pwd_reset_token=xxxx
    username: str,  # from /path/{username}
) -> User:
    """Returns User if one of the conditions is met.
    1. There is a pwd_reset_token passed as query parameter and it is valid OR
    2. authenticated_user is supersuser OR
    3. authenticated_user is User
    """
    target_user = get_user(username)  # The user we want to change the password
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        valid_pwd_reset_token = get_current_user(token=pwd_reset_token or "") == target_user
    except HTTPException:
        valid_pwd_reset_token = False

    try:
        authenticated_user = get_current_user(token="", request=request)
    except HTTPException:
        authenticated_user = None

    if any(
        [
            valid_pwd_reset_token,
            authenticated_user and authenticated_user.superuser,
            authenticated_user and authenticated_user.id == target_user.id,
        ]
    ):
        return target_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed to change this user's password",
    )


CanChangeUserPassword = Depends(get_user_if_change_password_is_allowed)


async def show_balance_field(
    *,
    request: Request,
    show_balance: Optional[bool] = False,  # from /user/?show_balance=true
) -> bool:
    """Returns True if one of the conditions is met.
    1. show_balance is True AND
    2. authenticated_user.superuser OR
    3. authenticated_user.username == username
    """
    if not show_balance:
        return False

    username = request.path_params.get("username")

    try:
        authenticated_user = get_current_user(token="", request=request)
    except HTTPException:
        authenticated_user = None

    if any(
        [
            authenticated_user and authenticated_user.superuser,
            authenticated_user and authenticated_user.username == username,
        ]
    ):
        return True

    return False


ShowBalanceField = Depends(show_balance_field)


def generate_password_key(size=4):
    """Generate a simple random password
    [0-9]
    """
    password = sample(digits, size)
    return "".join(password)
