# GraphQL FastAPI Boilerplate

![version](https://img.shields.io/badge/version-0.1.2-blue) ![python](https://img.shields.io/badge/python-3.8-blue) [![FastAPI](https://img.shields.io/badge/fastapi-0.63.0-brightgreen)](https://github.com/tiangolo/fastapi) [![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

This project is a boilerplate for FastaAPI GraphQL apps.

It's powered with:

- [FastAPI](https://github.com/tiangolo/fastapi) - main framework
- [Poetry](https://github.com/python-poetry/poetry) - dependency management
- [Invoke](https://github.com/pyinvoke/invoke) - task management
- [Dynaconf](https://github.com/rochacbruno/dynaconf) - configuration management
- [Loguru](https://github.com/Delgan/loguru) - logging system
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - ORM (1.4.0b1 with async capabilities)
- [Graphene](https://github.com/graphql-python/graphene) - GraphQL framework
- [pytest](https://github.com/pytest-dev/pytest) - tests


## How to start

Clone repo.

Install dependencies:
```sh
poetry env use 3.8
poetry install --no-root
```

Start dev containers (Redis and PostgreSQL):
```sh
docker-compose -f dev-compose.yaml up
```

Create local configuration file:
```sh
touch config/development.local.yaml
```

Set correct values for Redis and PostgreSQL connections (see `config/default.yaml` for example)

Activate venv:
```sh
poetry shell
```

Install pre-commit hooks (optional):
```sh
pre-commit install
```

Init new database and create your first user:
```sh
invoke db-upgrade
invoke create-user test test
```

Start dev server:
```sh
invoke dev
```

See urls for references and docs:
- http://localhost:8888/docs
- http://localhost:8888/graphql (you need auth in browser. I recommend [Requestly](https://chrome.google.com/webstore/detail/requestly-redirect-url-mo/mdnleldcmiljblolnjhpnblkcekpdkpa) extension for Chrome)

Enjoy!
