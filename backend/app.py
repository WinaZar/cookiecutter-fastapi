import uvicorn

from backend.app_factory import create_app
from backend.config import load_configuration

config = load_configuration()
app = create_app(config)

if __name__ == "__main__":
    uvicorn.run(
        "backend.app:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.debug,
        log_config=None,
    )
