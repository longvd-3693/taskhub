from datetime import timezone

from app.models.enums import TaskStatus
from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskResponse
from app.services.cache import CacheService
from app.core.config import settings


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository
        self.cache = CacheService()

    def _normalize_datetime(self, data: dict):
        due_date = data.get("due_date")

        if due_date is not None and due_date.tzinfo is not None:
            data["due_date"] = due_date.astimezone(timezone.utc).replace(tzinfo=None)

        return data

    def _tasks_cache_key(
        self,
        project_id: int,
        page: int,
        limit: int,
    ) -> str:
        return f"project:{project_id}:tasks:page:{page}:limit:{limit}"

    async def _invalidate_project_tasks_cache(
        self,
        project_id: int,
    ):
        await self.cache.delete_by_pattern(
            f"project:{project_id}:tasks:*"
        )

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

        task = await self.repository.create(data)

        await self._invalidate_project_tasks_cache(project_id)

        return task

    async def get_project_tasks(
        self,
        project_id: int,
        page: int = 1,
        limit: int = 20,
    ):
        cache_key = self._tasks_cache_key(
            project_id=project_id,
            page=page,
            limit=limit,
        )

        cached_tasks = await self.cache.get(cache_key)

        if cached_tasks is not None:
            return cached_tasks
        
        tasks = await self.repository.get_by_project(
            project_id=project_id,
            page=page,
            limit=limit,
        )

        serialized_tasks = [
            TaskResponse.model_validate(task).model_dump(mode="json")
            for task in tasks
        ]

        await self.cache.set(
            cache_key,
            serialized_tasks,
            expire_seconds=settings.task_cache_ttl,
        )

        return serialized_tasks

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

        updated_task = await self.repository.update(task, data)

        await self._invalidate_project_tasks_cache(updated_task.project_id)

        return updated_task

    async def delete_task(
        self,
        task: Task,
    ):
        project_id = task.project_id

        await self.repository.delete(task)

        await self._invalidate_project_tasks_cache(project_id)

        return True