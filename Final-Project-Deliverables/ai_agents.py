import os
import datetime
from openai import OpenAI
import Task_Management_Logic 
import Note_Management_Logic 

# --- AI Client Setup ---
# This setup is copied from our other modules
if "OPENAI_API_KEY" not in os.environ:
    CLIENT = None
else:
    CLIENT = OpenAI()
CHAT_MODEL = "gpt-4o-mini"
# --- End AI Client Setup ---

def get_daily_briefing():
    """
    Fetches all open tasks and uses an AI to generate a
    prioritized daily briefing.
    """
    if CLIENT is None:
        return "[red]Error: OPENAI_API_KEY not set. Cannot get briefing.[/red]"
    
    # 1. Retrieve data from our database via the managers
    todo_tasks = Task_Management_Logic.query_tasks(status='todo')
    doing_tasks = Task_Management_Logic.query_tasks(status='doing')
    
    # 2. Format the data for the AI
    # Convert the SQLite Row objects to simple strings
    today = datetime.date.today()
    task_list_str = "== TODO TASKS ==\n"
    if not todo_tasks:
        task_list_str += "No tasks 'todo'.\n"
    for task in todo_tasks:
        task_list_str += f"- ID {task['id']}: {task['title']} (Priority: {task['priority']}, Due: {task['due_date'] or 'N/A'})\n"
        
    task_list_str += "\n== DOING TASKS ==\n"
    if not doing_tasks:
        task_list_str += "No tasks 'doing'.\n"
    for task in doing_tasks:
        task_list_str += f"- ID {task['id']}: {task['title']} (Priority: {task['priority']}, Due: {task['due_date'] or 'N/A'})\n"

    # 3. Create the AI Prompt
    system_prompt = f"""
    You are a friendly and encouraging personal assistant. Today's date is {today.isoformat()}.
    Your goal is to provide a "Daily Briefing" for the user based on their task list.

    Follow these steps:
    1. Greet the user.
    2. Look at the 'TODO' and 'DOING' tasks provided.
    3. Identify any tasks that are "overdue" (due_date is before today).
    4. Identify any "high-priority" (Priority 1) tasks.
    5. Based on due dates and priority, suggest 1-3 "top priorities" for the day.
    6. Briefly list the other tasks.
    7. End with an encouraging message.
    
    Keep the tone concise, friendly, and helpful.
    """
    
    try:
        # 4. Call the Chat Completions API
        response = CLIENT.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_list_str} # Send the data as user content
            ],
            temperature=0.5, # A little more creative/friendly
            max_tokens=300
        )
        
        briefing = response.choices[0].message.content
        return briefing
        
    except Exception as e:
        print(f"Error during briefing: {e}")
        return "[red]Error: Failed to get briefing from AI.[/red]"