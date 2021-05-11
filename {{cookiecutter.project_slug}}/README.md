# {{cookiecutter.project_name}}

![python](https://img.shields.io/badge/python-3.9-blue) [![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

## Setup

Clone repo.

Install dependencies:
```sh
poetry env use 3.9
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
- http://localhost:8888/graphql (you need auth in browser. Recommend [Requestly](https://chrome.google.com/webstore/detail/requestly-redirect-url-mo/mdnleldcmiljblolnjhpnblkcekpdkpa) extension for Chrome)
