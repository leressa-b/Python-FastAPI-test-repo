from app.controllers import task_controller
from app.models.task import Task
import pytest

def test_create_and_delete_task():
    task = Task(id=1, title="Test", description="test desc", done=False)
    task_controller.create_task(task)
    all_tasks = task_controller.get_all_tasks()
    assert any(t.id == 1 for t in all_tasks)

def test_duplicate_task_creation():
    task = Task(id=2, title="Another", description="desc", done=False)
    task_controller.create_task(task)
    with pytest.raises(Exception):
        task_controller.create_task(task)
