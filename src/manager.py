"""
Todo Manager Module.

Contains the TodoManager class responsible for core application logic, task CRUD operations,
searching, filtering, sorting, and statistical calculations.
"""

from typing import List, Optional, Dict, Any
from .models import Task
from .storage import StorageManager


class TodoManager:
    """
    Manages the collection of tasks and handles business logic operations.
    """

    def __init__(self, storage: Optional[StorageManager] = None) -> None:
        """
        Initialize TodoManager with storage mechanism.

        Args:
            storage (StorageManager, optional): Storage manager for task persistence.
        """
        self.storage = storage or StorageManager()
        self.tasks: List[Task] = self.storage.load_tasks()

    def _get_next_id(self) -> int:
        """Calculate the next unique integer ID for a new task."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def save(self) -> bool:
        """Persist tasks to storage."""
        return self.storage.save_tasks(self.tasks)

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        due_date: str = "",
    ) -> Task:
        """
        Create and store a new task.

        Args:
            title (str): Title of the task.
            description (str): Detailed description.
            priority (str): Priority ('Low', 'Medium', 'High').
            due_date (str): Due date in 'YYYY-MM-DD' format.

        Returns:
            Task: The created task instance.
        """
        task_id = self._get_next_id()
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description.strip(),
            priority=priority,
            due_date=due_date,
            status="Pending",
        )
        self.tasks.append(task)
        self.save()
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks."""
        return list(self.tasks)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Optional[Task]: Task instance if found, None otherwise.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as completed by ID.

        Args:
            task_id (int): ID of the task to complete.

        Returns:
            bool: True if successful, False if task not found.
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.save()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id (int): ID of the task to delete.

        Returns:
            bool: True if task was deleted, False if task not found.
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save()
            return True
        return False

    def edit_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None,
    ) -> bool:
        """
        Edit details of an existing task. Fields set to None will remain unchanged.

        Args:
            task_id (int): Target task ID.
            title (str, optional): New title.
            description (str, optional): New description.
            priority (str, optional): New priority.
            due_date (str, optional): New due date.
            status (str, optional): New status ('Pending' / 'Completed').

        Returns:
            bool: True if task was updated, False if task not found.
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        if title is not None and title.strip():
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if priority is not None and priority.strip():
            norm_priority = priority.strip().capitalize()
            if norm_priority in Task.VALID_PRIORITIES:
                task.priority = norm_priority
        if due_date is not None:
            task.due_date = Task.normalize_date(due_date)
        if status is not None and status.strip():
            norm_status = status.strip().capitalize()
            if norm_status in Task.VALID_STATUSES:
                task.status = norm_status

        self.save()
        return True

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search for tasks matching a query string in title or description.

        Args:
            query (str): Keyword to search for.

        Returns:
            List[Task]: Matching task objects.
        """
        if not query or not query.strip():
            return list(self.tasks)
        q = query.strip().lower()
        return [
            task for task in self.tasks
            if q in task.title.lower() or q in task.description.lower()
        ]

    def filter_tasks(self, status: str) -> List[Task]:
        """
        Filter tasks by status ('Pending' or 'Completed').

        Args:
            status (str): Target status string.

        Returns:
            List[Task]: Filtered task list.
        """
        norm_status = status.strip().capitalize()
        return [task for task in self.tasks if task.status == norm_status]

    def sort_tasks(self, by: str = "due_date", reverse: bool = False) -> List[Task]:
        """
        Sort tasks by a specified attribute ('due_date', 'priority', 'id', 'created_at').

        Args:
            by (str): Attribute to sort by. Defaults to 'due_date'.
            reverse (bool): Reverse sort order if True.

        Returns:
            List[Task]: Sorted list of tasks.
        """
        if by == "due_date":
            # Push empty due dates to the end when ascending
            return sorted(
                self.tasks,
                key=lambda t: (t.due_date == "", t.due_date),
                reverse=reverse,
            )
        elif by == "priority":
            priority_map = {"High": 1, "Medium": 2, "Low": 3}
            return sorted(
                self.tasks,
                key=lambda t: priority_map.get(t.priority, 4),
                reverse=reverse,
            )
        elif by == "created_at":
            return sorted(self.tasks, key=lambda t: t.created_at, reverse=reverse)
        else:
            return sorted(self.tasks, key=lambda t: t.id, reverse=reverse)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate summary statistics for tasks.

        Returns:
            dict: Dictionary with total, completed, pending counts and completion percentage.
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == "Completed")
        pending = total - completed
        percentage = round((completed / total * 100), 1) if total > 0 else 0.0

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "percentage": percentage,
        }
