from fastapi import FastAPI

from app.api.v1.users import router as user_router
from app.core.lifespan import lifespan


app = FastAPI(
    title="TaskHub API",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(
    user_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "TaskHub API is running"
    }