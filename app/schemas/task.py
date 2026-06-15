from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    project_id: int
    assignee_id: int | None = None
    title: str
    description: str | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime | None = None
    created_by: int


class TaskUpdate(BaseModel):
    assignee_id: int | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    project_id: int
    assignee_id: int | None
    title: str
    description: str | None
    status: str
    priority: str
    due_date: datetime | None
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)