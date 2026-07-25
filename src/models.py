"""
Task Model Module.

Defines the Task data class and methods for data validation, status manipulation,
and serialization/deserialization to and from dictionary formats for JSON persistence.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class Task:
    """
    Represents a single task in the Todo List.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Concise title/summary of the task.
        description (str): Detailed explanation or notes for the task.
        priority (str): Priority level - 'Low', 'Medium', or 'High'.
        due_date (str): Due date in 'YYYY-MM-DD' format (or empty string if none).
        status (str): Current status - 'Pending' or 'Completed'.
        created_at (str): Timestamp of creation in 'YYYY-MM-DD HH:MM:SS' format.
    """

    id: int
    title: str
    description: str = ""
    priority: str = "Medium"
    due_date: str = ""
    status: str = "Pending"
    created_at: str = ""

    VALID_PRIORITIES = {"Low", "Medium", "High"}
    VALID_STATUSES = {"Pending", "Completed"}

    def __post_init__(self) -> None:
        """
        Validate and normalize fields after object initialization.
        Set creation date if not provided.
        """
        # Normalize priority casing
        normalized_priority = self.priority.strip().capitalize()
        if normalized_priority in self.VALID_PRIORITIES:
            self.priority = normalized_priority
        else:
            self.priority = "Medium"

        # Normalize status casing
        normalized_status = self.status.strip().capitalize()
        if normalized_status in self.VALID_STATUSES:
            self.status = normalized_status
        else:
            self.status = "Pending"

        # Set creation timestamp if empty
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Normalize due date format if present
        if self.due_date:
            self.due_date = self.normalize_date(self.due_date)

    @staticmethod
    def normalize_date(date_str: str) -> str:
        """
        Validates and formats a date string to 'YYYY-MM-DD'.
        Returns empty string if invalid.
        """
        if not date_str or not date_str.strip():
            return ""
        cleaned = date_str.strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(cleaned, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return cleaned  # Fallback to string if parsing fails

    def mark_completed(self) -> None:
        """Mark the task status as Completed."""
        self.status = "Completed"

    def mark_pending(self) -> None:
        """Mark the task status as Pending."""
        self.status = "Pending"

    def toggle_status(self) -> None:
        """Toggle status between Pending and Completed."""
        if self.status == "Completed":
            self.status = "Pending"
        else:
            self.status = "Completed"

    def to_dict(self) -> Dict[str, Any]:
        """Convert Task instance to a dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """
        Create a Task instance from a dictionary.

        Args:
            data (dict): Dictionary containing task attributes.

        Returns:
            Task: A new instance of Task.
        """
        return cls(
            id=int(data.get("id", 0)),
            title=str(data.get("title", "")),
            description=str(data.get("description", "")),
            priority=str(data.get("priority", "Medium")),
            due_date=str(data.get("due_date", "")),
            status=str(data.get("status", "Pending")),
            created_at=str(data.get("created_at", "")),
        )
