import os
import logging
import subprocess
from enum import Enum
from datetime import datetime

from .exceptions import TaskError

class TaskType(Enum):
    """Enum for task types"""
    CREATE_FOLDER = "CREATE_FOLDER"
    REMINDER = "REMINDER"
    RUN_COMMAND = "RUN_COMMAND"

class Task:
    """Represents a task with type, description, deadline, and status."""
    def __init__(self,task_type, deadline = None, description = "", is_completed = False):
        self.description = description
        self.deadline = deadline
        self.is_completed = is_completed
        self.task_type = task_type

    def  task_completed(self):
        self.is_completed = True

    def is_delayed(self):
        return datetime.now() >= self.deadline and not self.is_completed

    def do_task(self):
        try:
            if self.task_type == TaskType.CREATE_FOLDER:
                os.makedirs(self.description)
                logging.info("Folder created: %s",self.description)

            elif self.task_type == TaskType.REMINDER:
                command = (
                    f'schtasks /create /tn "TaskReminder_{self.description}" '
                    f'/tr "powershell.exe -NoProfile -Command '
                    f'[System.Reflection.Assembly]::LoadWithPartialName(\'System.Windows.Forms\'); '
                    f'[System.Windows.Forms.MessageBox]::Show(\'{self.description}\')" '  
                    f'/sc once /st {self.deadline.strftime("%H:%M")} '
                    f'/sd {self.deadline.strftime("%d/%m/%Y")}'
                )
                subprocess.run(command, shell = True, check = True)
                logging.info("Reminder set for %s",self.deadline)

            elif self.task_type == TaskType.RUN_COMMAND:
                os.system(self.description)
                logging.info("Executing command: %s",self.description)

            self.task_completed()
        except Exception as e:
            raise TaskError("Failed to execute task: %s" % self.description) from e
