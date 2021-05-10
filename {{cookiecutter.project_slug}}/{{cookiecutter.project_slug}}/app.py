import uvicorn

from {{cookiecutter.project_slug}}.app_factory import create_app
from {{cookiecutter.project_slug}}.config import load_configuration

config = load_configuration()
app = create_app(config)

if __name__ == "__main__":
    uvicorn.run(
        "{{cookiecutter.project_slug}}.app:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.debug,
        log_config=None,
    )
