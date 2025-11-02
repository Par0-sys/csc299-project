# Task2 — Task Manager Prototype Continuation

Improving upon task1, this file contains an iteration (V2) of a small command-line task manager used for the assignment described..

## What this does
- Stores tasks as JSON in `data/tasks.json` (created automatically).
- Provides a small CLI with commands: `add`, `list`, and `search`.
- Minimal task model: id, title, description, tags, status, created_at.

## Improvements Made
- Converted the simple list-based script into a small, clearer task model
    - Uses a task dataclass: id, title, description, tags, status, created_at.
    - Stores tasks in JSON (Still done automatically)
    - File format is {"tasks": [...]} making it easier to extend later.
- CLI Improvements
    - add: positional title, optional description, optional tags (Comma-seperated)
    - list: optional tag to filter
    - search: searches title, description and tags.
- Fucntions avaliable progammatically
    - add_task (title, description, tags) -> prints/returns Task.
    - read_tasks() -> list[Task]
    - list_tasks(tag) -> prints tasks
    - search_tasks(query) -> prints results

## Quick start (run from the `task2` directory)

# Add a task:

```powershell
python task_manager_V2.py add "Buy batteries" --desc "AA x4" --tags supplies,electronics
```

# List all tasks:

```powershell
python task_manager_V2.py list
```

# Filter by tag:

```powershell
python task_manager_V2.py list --tag electronics
```

# Search tasks:

```powershell
python task_manager_V2.py search batteries
```

# Notes for developers
- The JSON file is created automatically by the script in `task2/data/tasks.json`.
- The file format is:

```json
{
	"tasks": [
		{"id": 1, "title": "...", "description": "...", "tags": ["..."], "status": "pending", "created_at": "..."}
	]
}
```




