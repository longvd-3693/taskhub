from fastapi import FastAPI

from app.api.v1.users import router as user_router
from app.core.lifespan import lifespan
from app.api.v1.workspaces import router as workspace_router
from app.api.v1.projects import router as project_router
from app.api.v1.tasks import router as task_router
from app.api.v1.auth import router as auth_router
from app.middleware.process_time import ProcessTimeMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.exceptions.exceptions import AppException
from app.exceptions.handlers import app_exception_handler
from fastapi.exceptions import RequestValidationError

from app.exceptions.handlers import (
    internal_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="TaskHub API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    internal_exception_handler,
)

app.add_middleware(ProcessTimeMiddleware)

app.add_middleware(RequestIdMiddleware)


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