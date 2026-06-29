from fastapi import FastAPI
from app.routers.router_home import router as home_router
from app.config.settings import settings


app = FastAPI(
    name=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

app.include_router(home_router)