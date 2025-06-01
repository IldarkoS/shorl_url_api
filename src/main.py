from fastapi import FastAPI
from src.users.delivery.routers import router as users_router
app = FastAPI()


app.include_router(users_router, tags=["Users"], prefix="/users")