from typing import List, Optional
from app.models.task import Task, TaskFilter

class TaskService:
    def __init__(self, db):
        self.db = db

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        filter_params: Optional[TaskFilter] = None,
        user_id: Optional[int] = None
    ) -> List[Task]:
        return []