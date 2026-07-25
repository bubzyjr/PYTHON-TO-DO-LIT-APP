# 📝 Python Todo List Application

A complete, object-oriented command-line Todo List application built with **Python 3**. Features permanent JSON file storage, priority management, due dates, task filtering, sorting, searching, and real-time task statistics.

---

## 🚀 Features

- **➕ Add New Tasks**: Create tasks with title, description, priority (`Low`, `Medium`, `High`), and due date.
- **📋 View Tasks**: Clean tabular interface to list all tasks with statuses and due dates.
- **✏️ Edit / Update Tasks**: Modify task attributes or keep existing values easily.
- **✅ Complete Tasks**: Toggle status between `Pending` and `Completed`.
- **🗑️ Delete Tasks**: Remove unwanted tasks with safety confirmation prompts.
- **🔍 Search Tasks**: Search keywords in task titles and descriptions.
- **💾 JSON Persistence**: All data is saved automatically to `data/tasks.json` so data persists after exiting.
- **📅 Sort Tasks**: Sort tasks by Due Date, Priority, Creation Date, or Task ID.
- **🎯 Filter Tasks**: Filter tasks by status (`Pending` or `Completed`).
- **📊 Statistics & Progress**: View task completion rates, counts, and a visual progress bar.
- **🛡️ Input Validation & Safety**: Gracefully handles invalid inputs without crashing.

---

## 📁 Project Structure

```text
PYTHON TO-DO LIST/
├── main.py                  # Application entry point script
├── requirements.txt         # Project requirements specification
├── README.md                # Project documentation and guide
├── data/
│   └── tasks.json           # JSON database storage file
└── src/
    ├── __init__.py          # Package initialization
    ├── models.py            # Task data model (dataclass & serialization)
    ├── storage.py           # StorageManager class (JSON file read/write)
    ├── manager.py           # TodoManager class (core business logic & CRUD)
    └── cli.py               # CLIInterface class (interactive menu & prompt handlers)
```

---

## 📦 Requirements

- **Python**: Version 3.8 or higher.
- **Dependencies**: Built entirely using the **Python Standard Library** (`json`, `os`, `sys`, `datetime`, `typing`, `dataclasses`). No external `pip` installations are required.

---

## 🛠️ Installation & Setup

1. **Clone or Download** the project workspace directory:
   ```bash
   cd "PYTHON TO-DO LIST"
   ```

2. **Verify Python Installation**:
   ```bash
   python --version
   ```
   *(Ensure Python version is 3.8 or higher)*

---

## ▶️ How to Run

Run the entry point script using Python:

```bash
python main.py
```

---

## 💻 Example Usage

### Main Menu Interface

```text
==================================================
=================== ===== TODO APP ===== ===================
==================================================
1. View Tasks
2. Add Task
3. Edit Task
4. Complete Task
5. Delete Task
6. Search Task
7. Exit
====================
Enter your choice (1-7):
```

### Adding a Task

1. Select option `2` from the main menu.
2. Enter the task title: `Review Pull Requests`
3. Enter description: `Review PRs for API refactoring.`
4. Select priority: `3` (High)
5. Enter due date: `2026-07-28`

### Viewing Tasks & Statistics

Select option `1` -> `4` to view Task Statistics:

```text
==================================================
=============== TASK STATISTICS ================
==================================================
 Total Tasks:          4
 Completed Tasks:      1
 Pending Tasks:        3
 Completion Rate:      25.0%
 Progress:             [█████---------------] 25.0%
```

---

## 📄 Sample JSON Data Format

Tasks are stored in `data/tasks.json` using the following schema:

```json
[
    {
        "id": 1,
        "title": "Complete Python Todo List App",
        "description": "Implement OOP architecture, CLI interface, and JSON storage persistence.",
        "priority": "High",
        "due_date": "2026-07-30",
        "status": "Completed",
        "created_at": "2026-07-25 10:00:00"
    },
    {
        "id": 2,
        "title": "Prepare Weekly Project Status Report",
        "description": "Summarize key accomplishments, open risks, and next week priorities.",
        "priority": "Medium",
        "due_date": "2026-07-28",
        "status": "Pending",
        "created_at": "2026-07-25 11:30:00"
    }
]
```

---

## 🤝 Code Standards

This project complies strictly with **PEP 8** style guidelines, utilizes **Type Annotations** (`typing`), and adheres to **Object-Oriented Programming (OOP)** best practices.
