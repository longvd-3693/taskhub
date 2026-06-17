from pydantic import BaseModel, ConfigDict

from app.models.enums import WorkspaceMemberRole


class WorkspaceMemberCreate(BaseModel):
    user_id: int
    role: WorkspaceMemberRole


class WorkspaceMemberResponse(BaseModel):
    workspace_id: int
    user_id: int
    role: WorkspaceMemberRole

    model_config = ConfigDict(from_attributes=True)