from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task, TaskFilter
from app.services.task_service import TaskService
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

class TaskController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.task_service = TaskService(db)

    def get_all_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        filter_params: Optional[TaskFilter] = None,
        current_user: User = Depends(get_current_user)
    ) -> List[Task]:
        tasks = self.task_service.get_tasks(
            skip=skip,
            limit=skip + limit, 
            filter_params=filter_params,
            user_id=current_user.id
        )
        return tasks