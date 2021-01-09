import calendar
from datetime import datetime, timedelta
from typing import Optional

from authlib.jose import JWTClaims, jwt
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm.session import Session

from backend.config import Configuration
from backend.db.models import User


def is_password_valid(password: str, password_hash: str) -> bool:
    result: bool = pbkdf2_sha256.verify(password, password_hash)
    return result


def authenticate_user(session: Session, username: str, password: str) -> User:
    user: Optional[User] = session.query(User).filter_by(username=username).first()
    invalid_credentials_exception = HTTPException(
        status_code=400, detail="Incorrect username or password"
    )

    if user is None:
        raise invalid_credentials_exception

    if not is_password_valid(password, user.password):
        raise invalid_credentials_exception

    return user


def generate_jwt(config: Configuration, user: User) -> str:
    payload = {
        "iss": "GraphQLBackend",
        "sub": str(user.id),
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=config.jwt.expire_min),
    }
    header = {"alg": config.jwt.algorithm}
    token: bytes = jwt.encode(header, payload, config.secret_key)
    return token.decode("utf-8")


def decode_jwt(config: Configuration, token: str) -> JWTClaims:
    now = calendar.timegm(datetime.utcnow().utctimetuple())
    claims = jwt.decode(token, config.secret_key)
    claims.validate_exp(now, 0)
    return claims


def create_user(session: Session, username: str, password: str) -> User:
    hashed_password = pbkdf2_sha256.hash(password)
    db_user = User(username=username, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
