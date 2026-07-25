"""
Automated Verification Test Suite for Todo List Application.
"""

import os
import unittest
from src.models import Task
from src.storage import StorageManager
from src.manager import TodoManager


class TestTodoListApp(unittest.TestCase):
    def setUp(self):
        self.test_json = "data/test_tasks.json"
        if os.path.exists(self.test_json):
            os.remove(self.test_json)
        self.storage = StorageManager(filepath=self.test_json)
        self.manager = TodoManager(storage=self.storage)

    def tearDown(self):
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_add_and_get_task(self):
        task = self.manager.add_task(
            title="Test Task",
            description="Test Description",
            priority="High",
            due_date="2026-08-01",
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.status, "Pending")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)

    def test_complete_task(self):
        task = self.manager.add_task("Task to Complete")
        success = self.manager.complete_task(task.id)
        self.assertTrue(success)
        retrieved = self.manager.get_task_by_id(task.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.status, "Completed")

    def test_edit_task(self):
        task = self.manager.add_task("Initial Title", priority="Low")
        updated = self.manager.edit_task(task.id, title="Updated Title", priority="High")
        self.assertTrue(updated)
        retrieved = self.manager.get_task_by_id(task.id)
        self.assertEqual(retrieved.title, "Updated Title")
        self.assertEqual(retrieved.priority, "High")

    def test_delete_task(self):
        task = self.manager.add_task("Task to Delete")
        deleted = self.manager.delete_task(task.id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)

    def test_search_task(self):
        self.manager.add_task("Buy groceries", "Milk and Eggs")
        self.manager.add_task("Write code", "Python project")
        results = self.manager.search_tasks("groceries")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Buy groceries")

    def test_filter_tasks(self):
        t1 = self.manager.add_task("Task 1")
        t2 = self.manager.add_task("Task 2")
        self.manager.complete_task(t1.id)

        pending = self.manager.filter_tasks("Pending")
        completed = self.manager.filter_tasks("Completed")
        self.assertEqual(len(pending), 1)
        self.assertEqual(len(completed), 1)

    def test_statistics(self):
        t1 = self.manager.add_task("Task 1")
        t2 = self.manager.add_task("Task 2")
        self.manager.complete_task(t1.id)
        stats = self.manager.get_statistics()

        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 1)
        self.assertEqual(stats["percentage"], 50.0)

    def test_json_persistence(self):
        self.manager.add_task("Persistent Task", priority="High")

        # Create new manager reading same file
        new_manager = TodoManager(storage=self.storage)
        tasks = new_manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Persistent Task")


if __name__ == "__main__":
    unittest.main()
