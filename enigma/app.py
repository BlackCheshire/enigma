from fastapi import FastAPI
import uvicorn

from enigma.config import get_config
from enigma.controller import routers


app = FastAPI(title='Enigma')
for router in routers:
    app.include_router(router)


def run_app() -> None:
    cfg = get_config()
    uvicorn.run(
        app=app,
        host=cfg.app_host,
        port=cfg.app_port,
        log_level=cfg.app_log_level,
    )
