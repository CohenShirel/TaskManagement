import logging
import json
from datetime import datetime

from .task import Task, TaskType
from .exceptions import TaskFileNotFoundError, TaskError

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()]
)

class TaskManager:
    """Manages tasks including creation, execution...."""
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def execute_due_tasks(self):
        for task in self.tasks:
            if task.is_delayed():
                task.do_task()
        logging.info("Executed all due tasks.")

    def all_completed_tasks(self):
        completed_tasks = [task for task in self.tasks if task.is_completed]
        logging.info("Completed tasks:")
        for task in completed_tasks:
            logging.info(f"- {task.description}")

    def all_open_tasks(self):
        open_tasks = [task for task in self.tasks if not task.is_completed]
        logging.info("Open tasks:")
        for task in open_tasks:
            logging.info("-%s (Deadline: %s)",task.description, task.deadline)

    def save_to_file(self, file_name="tasks.json"):
        try:
            saved_task = []
            for task in self.tasks:
                saved_task.append({
                    "description": task.description,
                    "deadline": task.deadline.isoformat(),
                    "is_completed": task.is_completed,
                    "task_type": task.task_type.value,
                })
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(saved_task, file, indent=4)
        except Exception as e:
            raise TaskError("Failed to save tasks to %s: %s" % file_name % e) from e

    def load_from_file(self, file_name="tasks.json"):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                tasks_from_file = json.load(file)
                self.tasks = []
                for task in tasks_from_file:
                    current_task = Task(
                        description = task["description"],
                        deadline = datetime.fromisoformat(task["deadline"]) if task["deadline"] else None,
                        is_completed = task["is_completed"],
                        task_type = TaskType(task["task_type"]),
                    )
                    self.tasks.append(current_task)
        except FileNotFoundError as e:
            raise TaskFileNotFoundError("File %s not found." % file_name) from e
        except Exception as e:
            raise TaskError("An error occurred while loading tasks: %s" % e) from e
