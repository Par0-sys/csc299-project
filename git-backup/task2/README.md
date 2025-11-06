PKMS / Task2 — Task Manager Prototype

This folder contains an iteration (V2) of a small command-line task manager used for the PKMS assignment.

What this does
- Stores tasks as JSON in `data/tasks.json` (created automatically).
- Provides a small CLI with commands: `add`, `list`, and `search`.
- Minimal task model: id, title, description, tags, status, created_at.

Quick start (run from the `task2` directory)

Add a task:

```powershell
python task_manager_V2.py add "Buy batteries" --desc "AA x4" --tags supplies,electronics
```

List all tasks:

```powershell
python task_manager_V2.py list
```

Filter by tag:

```powershell
python task_manager_V2.py list --tag electronics
```

Search tasks:

```powershell
python task_manager_V2.py search batteries
```

Notes for developers
- The JSON file is created automatically by the script in `task2/data/tasks.json`.
- The file format is:

```json
{
	"tasks": [
		{"id": 1, "title": "...", "description": "...", "tags": ["..."], "status": "pending", "created_at": "..."}
	]
}
```

- If you add tests, put them under `task2/tests/` and run with `pytest` from the repo root or `task2` folder.

Suggested next enhancements
- Add commands to mark tasks complete or delete tasks.
- Add update/edit task command.
- Add nicer table output or export (CSV/Markdown).

Contact / author
Use the project workspace to iterate; if you want I can add tests and CI scaffolding next.
