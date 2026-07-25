"""
Storage Manager Module.

Handles loading tasks from and saving tasks to permanent JSON file storage.
Ensures directory structure exists and handles missing/corrupted files gracefully.
"""

import json
import os
from typing import List, Dict, Any
from .models import Task


class StorageManager:
    """
    Manages persistence of tasks using a JSON file.
    """

    def __init__(self, filepath: str = "data/tasks.json") -> None:
        """
        Initialize the StorageManager with a target JSON filepath.

        Args:
            filepath (str): Path to the JSON data file.
        """
        self.filepath = os.path.abspath(filepath)
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Create the parent directory for the JSON file if it does not exist."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def load_tasks(self) -> List[Task]:
        """
        Load tasks from the JSON file.

        Returns:
            List[Task]: A list of Task objects. Returns empty list if file doesn't exist or is invalid.
        """
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [Task.from_dict(item) for item in data if isinstance(item, dict)]
                return []
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Warning] Failed to load data from {self.filepath}: {e}")
            return []

    def save_tasks(self, tasks: List[Task]) -> bool:
        """
        Save a list of Task objects to the JSON file.

        Args:
            tasks (List[Task]): The list of Task instances to save.

        Returns:
            bool: True if save succeeded, False otherwise.
        """
        self._ensure_directory_exists()
        try:
            task_dicts = [task.to_dict() for task in tasks]
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(task_dicts, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[Error] Failed to save tasks to {self.filepath}: {e}")
            return False
