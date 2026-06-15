from datetime import timezone

from app.repositories.task import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def _normalize_datetime(self, data: dict):
        due_date = data.get("due_date")

        if due_date is not None and due_date.tzinfo is not None:
            data["due_date"] = due_date.astimezone(timezone.utc).replace(tzinfo=None)

        return data

    async def create_task(self, data: dict):
        data = self._normalize_datetime(data)
        return await self.repository.create(data)

    async def get_tasks(self, page: int = 1, limit: int = 20):
        return await self.repository.paginate(page=page, limit=limit)

    async def get_task(self, task_id: int):
        return await self.repository.get_by_id(task_id)

    async def update_task(self, task_id: int, data: dict):
        task = await self.repository.get_by_id(task_id)

        if task is None:
            return None

        data = self._normalize_datetime(data)

        return await self.repository.update(task, data)

    async def delete_task(self, task_id: int):
        task = await self.repository.get_by_id(task_id)

        if task is None:
            return False

        await self.repository.delete(task)
        return True