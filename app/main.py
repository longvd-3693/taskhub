from fastapi import FastAPI

from app.api.v1.users import router as user_router
from app.core.lifespan import lifespan
from app.api.v1.workspaces import router as workspace_router
from app.api.v1.projects import router as project_router
from app.api.v1.tasks import router as task_router
from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="TaskHub API",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(
    user_router,
    prefix="/api/v1"
)


app.include_router(
    workspace_router,
    prefix="/api/v1",
)


app.include_router(
    project_router, 
    prefix="/api/v1")


app.include_router(
    task_router, 
    prefix="/api/v1")

app.include_router(
    auth_router, 
    prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "TaskHub API is running"
    }