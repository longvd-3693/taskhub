from datetime import timezone

from app.models.enums import TaskStatus
from app.models.task import Task
from app.repositories.task import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def _normalize_datetime(self, data: dict):
        due_date = data.get("due_date")

        if due_date is not None and due_date.tzinfo is not None:
            data["due_date"] = due_date.astimezone(timezone.utc).replace(tzinfo=None)

        return data

    async def create_task(
        self,
        project_id: int,
        created_by: int,
        data: dict,
    ):
        data = self._normalize_datetime(data)
        data["project_id"] = project_id
        data["created_by"] = created_by
        data["status"] = TaskStatus.TODO

        return await self.repository.create(data)

    async def get_project_tasks(
        self,
        project_id: int,
        page: int = 1,
        limit: int = 20,
    ):
        return await self.repository.get_by_project(
            project_id=project_id,
            page=page,
            limit=limit,
        )

    async def get_task_with_project_workspace(
        self,
        task_id: int,
    ):
        return await self.repository.get_by_id_with_project_workspace(task_id)

    async def update_task(
        self,
        task: Task,
        data: dict,
    ):
        data = self._normalize_datetime(data)
        return await self.repository.update(task, data)

    async def delete_task(
        self,
        task: Task,
    ):
        await self.repository.delete(task)
        return True