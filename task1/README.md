Task Manager CLI

This is a small prototype command-line task manager that stores tasks in JSON.

Usage examples:

- Add a task:
  python task_manager.py add "Buy milk" --desc "2 liters" --tags shopping,groceries

- List tasks:
  python task_manager.py list

- List tasks with a tag:
  python task_manager.py list --tag groceries

- Search tasks:
  python task_manager.py search milk

Data is stored in `data/tasks.json` next to the script.
