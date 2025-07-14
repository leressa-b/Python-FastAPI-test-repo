from fastapi import APIRouter, Depends
from app.controllers import task_controller
from app.models.task import Task

router = APIRouter()

@router.get("/")
def get_tasks():
    return task_controller.get_all_tasks()

@router.post("/")
def create_task(task: Task):
    return task_controller.create_task(task)

@router.put("/{task_id}")
def update_task(task_id: int, task: Task):
    return task_controller.update_task(task_id, task)

@router.delete("/{task_id}")
def delete_task(task_id: int):
    return task_controller.delete_task(task_id)
