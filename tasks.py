# type: ignore
from invoke import task


@task
def dev(c):
    """
    Run development server
    """
    c.run("python -m backend.app", pty=True)


@task
def initdb(c):
    """
    Clear and init new database
    """
    c.run("python -m backend.cli initdb", pty=True)


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
