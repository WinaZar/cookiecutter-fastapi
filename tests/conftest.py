import pytest
from _pytest.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from backend.app_factory import create_app
from backend.auth.utils import create_user, generate_jwt
from backend.config import Configuration, load_configuration
from backend.db.models import Base, User


def pytest_configure(config: Config) -> None:
    app_config = load_configuration("testing")
    if app_config.tests.testcontainers:
        config.database_container = PostgresContainer(
            image="postgres:12",
            user="user",
            password="password",
            dbname="backend",
        )
        config.redis_container = RedisContainer(image="redis:alpine")
        config.database_container.start()
        config.redis_container.start()


def pytest_unconfigure(config: Config) -> None:
    app_config = load_configuration("testing")
    if app_config.tests.testcontainers:
        config.database_container.stop()
        config.redis_container.stop()


@pytest.fixture()
def test_config(pytestconfig: Config) -> Configuration:
    config = load_configuration("testing")
    if config.tests.testcontainers:
        config.database.dsn = (
            pytestconfig.database_container.get_connection_url().replace(
                "psycopg2", "asyncpg"
            )
        )
        redis_exposed_port = pytestconfig.redis_container.get_exposed_port(
            pytestconfig.redis_container.port_to_expose
        )
        config.cache.dsn = f"redis://localhost:{redis_exposed_port}"
    return config


@pytest.fixture()
def test_app(test_config: Configuration) -> FastAPI:
    return create_app(test_config)


@pytest.fixture()
def test_client(test_app: False) -> TestClient:
    return TestClient(test_app)


@pytest.fixture()
def database_session(pytestconfig: Config, test_config: Configuration) -> Session:
    if test_config.tests.testcontainers:
        db_url = pytestconfig.database_container.get_connection_url()
    else:
        db_url = test_config.database.dsn
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture()
def user(database_session: Session) -> User:
    username = "user"
    password = "password"
    return create_user(database_session, username, password)


@pytest.fixture()
def test_token(test_config: Configuration, user: User) -> str:
    return generate_jwt(test_config, user)
