import time
from typing import List, Optional
from app.models.task import Task, TaskFilter
from sqlalchemy.orm import Session
from app.db.database import TaskDB
class TaskService:
    def __init__(self, db:Session):
        self.db = db

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        filter_params: Optional[TaskFilter] = None,
        user_id: Optional[int] = None
    ) -> List[Task]:
        return []
    
    def update_task_status(self, task_id: int, new_status: str):
        task = self.db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            return None
        
        if task.status == "pending" and new_status == "in_progress":
            current_status = task.status
            
            time.sleep(0.2) 
            
            if current_status == task.status:
                task.status = new_status
                self.db.commit()
                self.db.refresh(task)
                return task
        

        task.status = new_status
        self.db.commit()
        self.db.refresh(task)
        return task