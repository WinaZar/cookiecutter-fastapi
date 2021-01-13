# type: ignore
from invoke import task


@task
def dev(c):
    """
    Run development server
    """
    c.run("python -m backend.app", pty=True)


@task
def db_upgrade(c):
    """
    Apply alembic migrations
    """
    c.run("PYTHONPATH=. alembic upgrade head", pty=True)


@task
def generate_migration(c, message):
    """
    Generate new migration with alembic
    """
    c.run(f"PYTHONPATH=. alembic revision --autogenerate -m '{message}'")


@task
def create_user(c, username, password):
    """
    Create new user in database
    """
    c.run(f"python -m backend.cli create-new-user {username} {password}", pty=True)


@task
def test(c):
    """
    Run tests
    """
    c.run("pytest -v", pty=True)
