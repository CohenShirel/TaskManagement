import pytest
from datetime import datetime, timedelta

from tasks.task import Task, TaskType
from tasks.task_manager import TaskManager
from tasks.exceptions import TaskFileNotFoundError

####### Test of task.py #######
def test_task_addition():
    task = Task(TaskType.REMINDER, datetime.now() + timedelta(days = 1), "Test Reminder")
    assert task.description == "Test Reminder"
    assert task.is_completed == False
    assert task.task_type == TaskType.REMINDER

def test_task_is_delayed():
    task = Task(TaskType.REMINDER, datetime.now() - timedelta(days = 1), "Past Reminder")
    assert task.is_delayed() == True

def test_task_completion():
    task = Task(TaskType.REMINDER, datetime.now() + timedelta(days = 1), "Test Reminder")
    task.task_completed()
    assert task.is_completed == True

####### Test of task_manager.py #######
def test_add_task():
    manager = TaskManager()
    task = Task(TaskType.CREATE_FOLDER, datetime.now() + timedelta(days = 1), "Test Folder")
    manager.add_task(task)
    assert len(manager.tasks) == 1
    assert manager.tasks[0].description == "Test Folder"

def test_execute_due_tasks():
    manager = TaskManager()
    task = Task(TaskType.REMINDER, datetime.now() - timedelta(days = 1), "Past Task")
    manager.add_task(task)
    manager.execute_due_tasks()
    assert task.is_completed == True

def test_save_and_load_tasks(tmp_path):
    manager = TaskManager()
    file_path = tmp_path / "tasks.json"

    task = Task(TaskType.REMINDER, datetime.now() + timedelta(days = 1), "Test Reminder")
    manager.add_task(task)
    manager.save_to_file(file_name = str(file_path))

    new_manager = TaskManager()
    new_manager.load_from_file(file_name = str(file_path))
    assert len(new_manager.tasks) == 1
    assert new_manager.tasks[0].description == "Test Reminder"

def test_load_file_not_found():
    manager = TaskManager()
    with pytest.raises(TaskFileNotFoundError):
        manager.load_from_file(file_name = "non_existing_file.json")
