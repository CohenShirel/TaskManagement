import argparse
import logging
from datetime import datetime

from tasks.task_manager import TaskManager
from tasks.task import Task, TaskType
from tasks.exceptions import TaskFileNotFoundError, TaskError

def main():
    parser = argparse.ArgumentParser(description = "Task Manager CLI")
    parser.add_argument("--addtask", type = str, help = "Add a new task description")
    parser.add_argument("--type", type = str, choices = ["CREATE_FOLDER", "REMINDER", "RUN_COMMAND"], help = "Task type")
    parser.add_argument("--deadline", type = str, help = "Deadline for the task (format: YYYY-MM-DD HH:MM)")
    parser.add_argument("--listopentasks", action = "store_true", help = "List all open tasks")
    parser.add_argument("--listcompletedtasks", action = "store_true", help = "List all completed tasks")
    parser.add_argument("--execute-due", action = "store_true", help = "Execute due tasks")

    args = parser.parse_args()
    manager = TaskManager()

    try:
        manager.load_from_file()
    except TaskFileNotFoundError:
        logging.warning("Tasks file not found. Starting with an empty task list.")
    except TaskError as e:
        logging.error("Failed to load tasks: %s", e)
    except Exception as e:
        logging.error("Unexpected error while loading tasks: %s", e)

    if args.addtask and args.type and args.deadline:
        try:
            deadline = datetime.strptime(args.deadline, "%Y-%m-%d %H:%M")
            current_task = Task(
                task_type = TaskType(args.type),
                description = args.addtask if args.addtask else "",
                deadline = deadline
            )
            manager.add_task(current_task)
            current_task.do_task()

        except ValueError:
            logging.error("Invalid deadline format. Use YYYY-MM-DD HH:MM.")
        except Exception as e:
            logging.error("Unexpected error while adding task: %s", e)
    elif args.listopentasks:
        manager.all_open_tasks()
    elif args.listcompletedtasks:
        manager.all_completed_tasks()
    elif args.execute_due:
        manager.execute_due_tasks()

    try:
        manager.save_to_file()
    except TaskError as e:
        logging.error("Failed to save tasks: %s", e)
    except Exception as e:
        logging.error("Unexpected error while saving tasks: %s", e)

if __name__ == "__main__":
    main()