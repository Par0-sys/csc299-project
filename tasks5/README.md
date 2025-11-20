# Simple CLI Task Manager

This repository contains a small Python command-line task manager that stores tasks in `tasks.txt` and completed tasks in `completed.txt`.

Usage (PowerShell / cmd):

```powershell
# Add a task
python tasks.py add "Buy milk"

# Or interactively:
python tasks.py add
# then type the task and press Enter

# List tasks
python tasks.py list

# Complete a task by its number (as shown by list)
python tasks.py complete 1
```

Files created/used:

- `tasks.py` - the CLI script
- `tasks.txt` - plain text file where active tasks are stored (created on-demand)
- `completed.txt` - append-only file that stores completed tasks with timestamps

Notes:

- Tasks are stored one per line in `tasks.txt`.
- Completing a task removes it from `tasks.txt` and appends it with a timestamp to `completed.txt`.
