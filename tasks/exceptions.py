"""Module defining exceptions for the task management system."""

class TaskError(Exception):
    """Base class for all task exceptions."""

class TaskFileNotFoundError(TaskError):
    """Raised when the tasks file is not found."""
