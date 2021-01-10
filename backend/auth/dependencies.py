from typing import Optional

from authlib.jose.errors import (
    BadSignatureError,
    DecodeError,
    ExpiredTokenError,
    InvalidClaimError,
)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.auth.utils import decode_jwt
from backend.config import Configuration
from backend.db.dependencies import get_session
from backend.db.models import User
from backend.dependencies import get_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(
    session: AsyncSession = Depends(get_session),
    config: Configuration = Depends(get_config),
    token: str = Depends(oauth2_scheme),
) -> User:
    authenticate_failed = HTTPException(
        status_code=401,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_claims = decode_jwt(config, token)
    except (BadSignatureError, InvalidClaimError, ExpiredTokenError, DecodeError):
        raise authenticate_failed
    user_id = int(jwt_claims["sub"])
    query_result = await session.execute(select(User).filter_by(id=user_id))
    user: Optional[User] = query_result.one_or_none()
    if user is None:
        raise authenticate_failed
    return user
