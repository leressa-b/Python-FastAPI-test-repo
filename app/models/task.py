from pydantic import BaseModel, validator
from typing import Optional, List
from enum import Enum
from datetime import datetime
from app.models.base import BaseDBModel

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: List[str] = []
    
    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters long')
        return v.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

class TaskInDB(TaskBase, BaseDBModel):
    owner_id: int
    assigned_to: Optional[int] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None

class Task(TaskBase, BaseDBModel):
    owner_id: int
    assigned_to: Optional[int] = None

class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    owner_id: Optional[int] = None
    assigned_to: Optional[int] = None
    tags: Optional[List[str]] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None