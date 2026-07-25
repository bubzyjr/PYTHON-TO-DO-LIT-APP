"""
CLI Interface Module.

Provides an interactive command-line interface for the Todo List application.
Handles user navigation, menu rendering, task display formatting, and input validation.
"""

import sys
from typing import List, Optional
from .models import Task
from .manager import TodoManager


class CLIInterface:
    """
    Command Line Interface class to interact with the user.
    """

    def __init__(self, manager: TodoManager) -> None:
        """
        Initialize CLI Interface with TodoManager.

        Args:
            manager (TodoManager): Instance of TodoManager to perform operations.
        """
        self.manager = manager

    def run(self) -> None:
        """Main application loop displaying the main menu and handling choices."""
        while True:
            self._print_header("===== TODO APP =====")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Edit Task")
            print("4. Complete Task")
            print("5. Delete Task")
            print("6. Search Task")
            print("7. Exit")
            print("=" * 20)

            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                self._handle_view_tasks()
            elif choice == "2":
                self._handle_add_task()
            elif choice == "3":
                self._handle_edit_task()
            elif choice == "4":
                self._handle_complete_task()
            elif choice == "5":
                self._handle_delete_task()
            elif choice == "6":
                self._handle_search_task()
            elif choice == "7":
                print("\nThank you for using Todo App! Goodbye.\n")
                sys.exit(0)
            else:
                print("\n[!] Invalid choice. Please enter a number from 1 to 7.")
                self._pause()

    def _print_header(self, title: str) -> None:
        """Helper to print standardized section headers."""
        print("\n" + "=" * 50)
        print(f" {title} ".center(50, "="))
        print("=" * 50)

    def _pause(self) -> None:
        """Prompt user to press Enter to return to main menu."""
        input("\nPress Enter to return to the main menu...")

    def _display_task_table(self, tasks: List[Task], title: str = "TASKS LIST") -> None:
        """
        Render a list of tasks in a clean tabular view.

        Args:
            tasks (List[Task]): Tasks to display.
            title (str): Header title.
        """
        if not tasks:
            print("\n[i] No tasks found.")
            return

        print(f"\n--- {title} ({len(tasks)}) ---")
        header = f"{'ID':<4} | {'Status':<11} | {'Priority':<8} | {'Due Date':<10} | {'Title':<25}"
        divider = "-" * len(header)
        print(divider)
        print(header)
        print(divider)

        for task in tasks:
            status_icon = "[x] Done" if task.status == "Completed" else "[ ] Pending"
            due = task.due_date if task.due_date else "N/A"
            title_truncated = task.title[:22] + "..." if len(task.title) > 25 else task.title
            print(f"{task.id:<4} | {status_icon:<11} | {task.priority:<8} | {due:<10} | {title_truncated:<25}")

        print(divider)

    def _display_task_details(self, task: Task) -> None:
        """Display detailed view for a single task."""
        print("\n" + "-" * 40)
        print(f" Task Details (ID: {task.id}) ".center(40, "-"))
        print(f" Title:       {task.title}")
        print(f" Description: {task.description or '(No description)'}")
        print(f" Priority:    {task.priority}")
        print(f" Status:      {task.status}")
        print(f" Due Date:    {task.due_date or 'None'}")
        print(f" Created At:  {task.created_at}")
        print("-" * 40)

    def _handle_view_tasks(self) -> None:
        """Sub-menu for viewing, filtering, sorting tasks and viewing statistics."""
        while True:
            self._print_header("VIEW TASKS")
            print("1. View All Tasks")
            print("2. Filter Tasks (Pending / Completed)")
            print("3. Sort Tasks (by Due Date, Priority, etc.)")
            print("4. View Task Statistics")
            print("5. View Full Task Details")
            print("6. Back to Main Menu")

            choice = input("\nEnter choice (1-6): ").strip()

            if choice == "1":
                tasks = self.manager.get_all_tasks()
                self._display_task_table(tasks, "ALL TASKS")
                self._pause()
                break
            elif choice == "2":
                self._handle_filter_sub_menu()
                break
            elif choice == "3":
                self._handle_sort_sub_menu()
                break
            elif choice == "4":
                self._handle_show_statistics()
                break
            elif choice == "5":
                self._handle_view_single_detail()
                break
            elif choice == "6":
                break
            else:
                print("\n[!] Invalid option. Please enter 1-6.")

    def _handle_filter_sub_menu(self) -> None:
        """Sub-menu for filtering tasks by status."""
        print("\nFilter Status:")
        print("1. Pending Tasks")
        print("2. Completed Tasks")
        filter_choice = input("Select filter (1-2): ").strip()

        if filter_choice == "1":
            filtered = self.manager.filter_tasks("Pending")
            self._display_task_table(filtered, "PENDING TASKS")
        elif filter_choice == "2":
            filtered = self.manager.filter_tasks("Completed")
            self._display_task_table(filtered, "COMPLETED TASKS")
        else:
            print("\n[!] Invalid filter selection.")
        self._pause()

    def _handle_sort_sub_menu(self) -> None:
        """Sub-menu for sorting tasks."""
        print("\nSort Tasks By:")
        print("1. Due Date")
        print("2. Priority (High -> Low)")
        print("3. Creation Date")
        print("4. ID")
        sort_choice = input("Select sort option (1-4): ").strip()

        sort_key_map = {
            "1": "due_date",
            "2": "priority",
            "3": "created_at",
            "4": "id",
        }

        if sort_choice in sort_key_map:
            sorted_tasks = self.manager.sort_tasks(by=sort_key_map[sort_choice])
            self._display_task_table(sorted_tasks, f"SORTED BY {sort_key_map[sort_choice].upper()}")
        else:
            print("\n[!] Invalid sort option.")
        self._pause()

    def _handle_show_statistics(self) -> None:
        """Display overall task statistics."""
        stats = self.manager.get_statistics()
        self._print_header("TASK STATISTICS")
        print(f" Total Tasks:          {stats['total']}")
        print(f" Completed Tasks:      {stats['completed']}")
        print(f" Pending Tasks:        {stats['pending']}")
        print(f" Completion Rate:      {stats['percentage']}%")

        # Visual progress bar using standard ASCII characters for cross-platform safety
        bar_length = 20
        filled_length = int(bar_length * stats['percentage'] // 100)
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(f" Progress:             [{bar}] {stats['percentage']}%")
        self._pause()

    def _handle_view_single_detail(self) -> None:
        """Display detailed view for a selected task ID."""
        task_id = self._prompt_int("Enter Task ID to view details: ")
        if task_id is not None:
            task = self.manager.get_task_by_id(task_id)
            if task:
                self._display_task_details(task)
            else:
                print(f"\n[!] Task with ID {task_id} not found.")
        self._pause()

    def _handle_add_task(self) -> None:
        """Handle creating a new task."""
        self._print_header("ADD NEW TASK")

        title = input("Enter Task Title (required): ").strip()
        while not title:
            print("[!] Task title cannot be empty.")
            title = input("Enter Task Title (required): ").strip()

        description = input("Enter Description (optional): ").strip()

        print("Select Priority:")
        print("1. Low")
        print("2. Medium (Default)")
        print("3. High")
        pri_choice = input("Enter choice (1-3) [Default 2]: ").strip()
        priority_map = {"1": "Low", "2": "Medium", "3": "High"}
        priority = priority_map.get(pri_choice, "Medium")

        due_date = input("Enter Due Date (YYYY-MM-DD) (optional): ").strip()
        if due_date:
            due_date = Task.normalize_date(due_date)

        task = self.manager.add_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        print(f"\n[✓] Task successfully created with ID #{task.id}!")
        self._pause()

    def _handle_edit_task(self) -> None:
        """Handle editing an existing task."""
        self._print_header("EDIT TASK")
        all_tasks = self.manager.get_all_tasks()
        if not all_tasks:
            print("\n[i] No tasks available to edit.")
            self._pause()
            return

        self._display_task_table(all_tasks, "SELECT TASK TO EDIT")
        task_id = self._prompt_int("Enter Task ID to edit (or 0 to cancel): ")

        if task_id is None or task_id == 0:
            return

        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"\n[!] Task ID {task_id} not found.")
            self._pause()
            return

        self._display_task_details(task)
        print("\nLeave input blank to keep existing value.")

        new_title = input(f"New Title [{task.title}]: ").strip()
        new_desc = input(f"New Description [{task.description or 'None'}]: ").strip()

        print(f"Current Priority: {task.priority}")
        print("1. Low | 2. Medium | 3. High | Enter to keep current")
        pri_input = input("New Priority choice (1-3): ").strip()
        pri_map = {"1": "Low", "2": "Medium", "3": "High"}
        new_priority = pri_map.get(pri_input, task.priority)

        new_due = input(f"New Due Date (YYYY-MM-DD) [{task.due_date or 'None'}]: ").strip()

        status_input = input(f"Status (1. Pending / 2. Completed) [{task.status}]: ").strip()
        status_map = {"1": "Pending", "2": "Completed"}
        new_status = status_map.get(status_input, task.status)

        updated = self.manager.edit_task(
            task_id=task_id,
            title=new_title if new_title else None,
            description=new_desc if new_desc else None,
            priority=new_priority,
            due_date=new_due if new_due else None,
            status=new_status,
        )

        if updated:
            print(f"\n[✓] Task #{task_id} updated successfully!")
        else:
            print(f"\n[!] Failed to update task #{task_id}.")
        self._pause()

    def _handle_complete_task(self) -> None:
        """Handle marking a task as complete."""
        self._print_header("MARK TASK COMPLETED")
        pending_tasks = self.manager.filter_tasks("Pending")
        if not pending_tasks:
            print("\n[i] No pending tasks to complete.")
            self._pause()
            return

        self._display_task_table(pending_tasks, "PENDING TASKS")
        task_id = self._prompt_int("Enter Task ID to mark as Completed (or 0 to cancel): ")

        if task_id is None or task_id == 0:
            return

        if self.manager.complete_task(task_id):
            print(f"\n[✓] Task #{task_id} marked as Completed!")
        else:
            print(f"\n[!] Task ID {task_id} not found.")
        self._pause()

    def _handle_delete_task(self) -> None:
        """Handle deleting a task."""
        self._print_header("DELETE TASK")
        all_tasks = self.manager.get_all_tasks()
        if not all_tasks:
            print("\n[i] No tasks available to delete.")
            self._pause()
            return

        self._display_task_table(all_tasks, "ALL TASKS")
        task_id = self._prompt_int("Enter Task ID to delete (or 0 to cancel): ")

        if task_id is None or task_id == 0:
            return

        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"\n[!] Task ID {task_id} not found.")
            self._pause()
            return

        confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/N): ").strip().lower()
        if confirm == "y":
            if self.manager.delete_task(task_id):
                print(f"\n[✓] Task #{task_id} deleted successfully.")
            else:
                print(f"\n[!] Failed to delete task #{task_id}.")
        else:
            print("\n[i] Deletion cancelled.")
        self._pause()

    def _handle_search_task(self) -> None:
        """Handle searching tasks by keyword."""
        self._print_header("SEARCH TASKS")
        keyword = input("Enter keyword to search (title or description): ").strip()
        if not keyword:
            print("\n[!] Keyword cannot be empty.")
            self._pause()
            return

        results = self.manager.search_tasks(keyword)
        self._display_task_table(results, f"SEARCH RESULTS FOR '{keyword}'")
        self._pause()

    def _prompt_int(self, prompt_text: str) -> Optional[int]:
        """Safely prompt the user for an integer input."""
        user_input = input(prompt_text).strip()
        if not user_input:
            return None
        try:
            return int(user_input)
        except ValueError:
            print("\n[!] Invalid input. Please enter a numeric ID.")
            return None
