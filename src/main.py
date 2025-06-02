from fastapi import FastAPI

from src.core.exception_handler import setup_exception_handler
from src.urls.delivery.routers import router as short_urls_router
from src.users.delivery.routers import router as users_router

app = FastAPI()


setup_exception_handler(app)
app.include_router(users_router, tags=["Users and Auth"], prefix="/users")
app.include_router(short_urls_router, tags=["ShortURL"])
