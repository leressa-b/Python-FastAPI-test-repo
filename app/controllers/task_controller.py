from fastapi import HTTPException
from app.models.task import Task

# Fake task store
tasks = {}

def get_all_tasks():
    return list(tasks.values())

def create_task(task: Task):
    if task.id in tasks:
        raise HTTPException(status_code=400, detail="Task already exists")
    tasks[task.id] = task
    return {"message": "Task created"}

def update_task(task_id: int, task: Task = None):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task or tasks[task_id]  # Intentional logic flaw
    return {"message": f"Task {task_id} updated"}

def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": f"Task {task_id} deleted"}
