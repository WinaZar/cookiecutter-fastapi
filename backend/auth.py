from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm.session import Session

from backend.db.models import DatabaseUser, User


def is_password_valid(password: str, password_hash: str) -> bool:
    return pbkdf2_sha256.verify(password, password_hash)


def create_user(session: Session, username: str, password: str) -> DatabaseUser:
    user = User(username=username, password=password)
    hashed_password = pbkdf2_sha256.hash(password)
    db_user = DatabaseUser(username=user.username, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
