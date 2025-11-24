import sqlite3
from pathlib import Path
import datetime  # NEW: For sending today's date to AI
import json      # NEW: To parse AI response
import os        # NEW: To check for API key
from openai import OpenAI  # NEW: To call OpenAI

# --- Setup ---
DB_FILE = Path(__file__).parent / "my_system.db"

# AI Client Setup (mirrors note_manager.py)
if "OPENAI_API_KEY" not in os.environ:
    CLIENT = None
else:
    CLIENT = OpenAI()
CHAT_MODEL = "gpt-4o-mini"


def add_task(title, description=None, priority=3, due_date=None):
    """Adds a new task to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    sql = "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)"
    
    try:
        cursor.execute(sql, (title, description, priority, due_date))
        conn.commit()
        print(f"Added task: '{title}'")
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
    finally:
        conn.close()

# --- AI Task Parsing Agent ---
def add_task_from_natural_language(text):
    """
    Uses an AI model to parse natural language text into a structured task.
    """
    if CLIENT is None:
        print("[red]Error: OPENAI_API_KEY not set. Cannot use smart add.[/red]")
        return
        
    # Give the AI today's date for context (to understand "tomorrow", "next Friday")
    today = datetime.date.today().isoformat()
    
    system_prompt = f"""
    You are a task parsing assistant. Today's date is {today}.
    Parse the user's text into a JSON object with the following fields:
    - "title": (string) The main title of the task.
    - "description": (string or null) Any extra details.
    - "priority": (integer) 1 (high), 2 (medium), or 3 (low/default). Infer from words like "important", "urgent" (1), or "casual" (3).
    - "due_date": (string or null) The due date in 'YYYY-MM-DD' format.

    Rules:
    - Only return a single, valid JSON object.
    - If a field is not mentioned, use null (or 3 for priority).
    - Be smart about dates: "tomorrow" is { (datetime.date.today() + datetime.timedelta(days=1)).isoformat() }.
    
    Example:
    User: "buy milk tomorrow morning #urgent"
    JSON: {{"title": "buy milk", "description": "buy in the morning", "priority": 1, "due_date": "{(datetime.date.today() + datetime.timedelta(days=1)).isoformat()}"}}
    """
    
    try:
        response = CLIENT.chat.completions.create(
            model=CHAT_MODEL,
            response_format={"type": "json_object"}, # Force JSON output
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        
        # Parse the JSON response
        task_data = json.loads(response.choices[0].message.content)
        
        # Get data, providing defaults
        title = task_data.get("title")
        if not title:
            print("[red]AI could not determine a title. Task not added.[/red]")
            return

        desc = task_data.get("description")
        priority = task_data.get("priority", 3)
        due_date = task_data.get("due_date")
        
        # Call the original add_task function
        add_task(title, desc, priority, due_date)
        print(f"[AI] Successfully added: '{title}' (Priority: {priority}, Due: {due_date or 'None'})")

    except Exception as e:
        print(f"[red]Error during smart add: {e}[/red]")


def query_tasks(status=None, priority=None):
    """
    Finds tasks, optionally filtering by status or priority.
    Returns results as dictionary-like rows.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This is key for easy access
    cursor = conn.cursor()
    
    sql = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if status:
        sql += " AND status = ?"
        params.append(status)
    if priority:
        sql += " AND priority = ?"
        params.append(priority)
        
    sql += " ORDER BY priority, due_date"
    
    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    return results

def update_task_status(task_id, new_status):
    """Updates a task's status (e.g., 'todo' -> 'done')."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    sql = "UPDATE tasks SET status = ? WHERE id = ?"
    try:
        cursor.execute(sql, (new_status, task_id))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Updated task {task_id} to '{new_status}'")
    except sqlite3.Error as e:
        print(f"Error updating task: {e}")
    finally:
        conn.close()

def delete_task(task_id):
    """Deletes a task from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    sql = "DELETE FROM tasks WHERE id = ?"
    try:
        cursor.execute(sql, (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Error: No task found with ID {task_id}")
        else:
            print(f"Deleted task {task_id}")
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")
    finally:
        conn.close()