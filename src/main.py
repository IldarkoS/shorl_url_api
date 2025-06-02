from fastapi import FastAPI
from src.users.delivery.routers import router as users_router
from src.short_urls.delivery.routers import router as short_urls_router

app = FastAPI()


app.include_router(users_router, tags=["Users and Auth"], prefix="/users")
app.include_router(short_urls_router, tags=["ShortURL"])