from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import Database_initializer
import Task_Management_Logic
import Note_Management_Logic
import ai_agents

# Setup rich console
console = Console()

def print_help():
    """Prints the main help menu."""
    console.print("\n[bold cyan]Personal AI Assistant Menu[/bold cyan]")
    console.print("[yellow]Tasks:[/yellow]")
    console.print("  [bold]smart add [text...][/bold] - (AI) Add a task with natural language") 
    console.print("  [bold]add task detailed[/bold] - Add a new task (step-by-step)") 
    console.print("  [bold]list tasks [filter][/bold] - List tasks. Filter by: todo, doing, done, high, medium, low")
    console.print("  [bold]done [ID][/bold]         - Mark task [ID] as 'done'")
    console.print("  [bold]del task [ID][/bold]     - Delete task [ID]")
    console.print("[yellow]Notes (PKMS):[/yellow]")
    console.print("  [bold]add note[/bold]    - Add a new note (will be embedded)")
    console.print("  [bold]find tag [TAG][/bold] - Find notes by tag")
    console.print("  [bold]find similar[/bold] - (Smart Search) Find notes by meaning")
    console.print("  [bold]get note [ID][/bold]  - Get note by its ID")
    console.print("  [bold]summarize note [ID][/bold] - (AI) Summarize note [ID]")
    console.print("[yellow]General:[/yellow]")
    console.print("  [bold]brief me[/bold]     - (AI) Get a daily briefing")
    console.print("  [bold]help[/bold]         - Show this menu")
    console.print("  [bold]exit[/bold]         - Quit the application")

def handle_add_task():
    """Guides user through adding a new task."""
    # --- UPDATED: Replaced Prompt.ask with input() ---
    title = input("Task Title: ")
    desc = input("Description (optional): ")
    priority = input("Priority (1-3) [default: 3]: ")
    due_date = input("Due Date (YYYY-MM-DD) (optional): ")
    
    # Handle default priority
    if not priority:
        priority = "3"
    # --- END UPDATE ---
    
    Task_Management_Logic.add_task(title, desc or None, int(priority), due_date or None)

def handle_smart_add(command):
    """
    Extracts the natural language text and sends it to the task parser.
    """
    try:
        # Get everything after "smart add "
        text = command.split(" ", 2)[2]
        console.print(f"[yellow]Parsing task: '{text}'...[/yellow]")
        Task_Management_Logic.add_task_from_natural_language(text)
    except IndexError:
        console.print("[red]Error: Please provide text. (e.g., smart add Buy milk tomorrow)[/red]")

def handle_list_tasks(command):
    """Retrieves and prints all tasks in a table, with optional filtering."""
    
    # --- UPDATED: More robust parsing ---
    parts = command.split() # split() with no args handles extra spaces
    filter_word = None
    if len(parts) == 3: # e.g., ['list', 'tasks', 'todo']
        filter_word = parts[2].lower()
    # --- END UPDATE ---

    status_filter = None
    priority_filter = None
    table_title = "All Tasks"

    if filter_word in ['todo', 'doing', 'done']:
        status_filter = filter_word
        table_title = f"Tasks: {filter_word.upper()}"
    elif filter_word == 'high':
        priority_filter = 1
        table_title = "Tasks: High Priority"
    elif filter_word == 'medium':
        priority_filter = 2
        table_title = "Tasks: Medium Priority"
    elif filter_word == 'low':
        priority_filter = 3
        table_title = "Tasks: Low Priority"
    elif filter_word is not None:
        console.print(f"[red]Error: Unknown filter '{filter_word}'. Showing all tasks.[/red]")


    tasks = Task_Management_Logic.query_tasks(status=status_filter, priority=priority_filter)
    if not tasks:
        console.print(f"[yellow]No tasks found matching '{filter_word or 'all'}'.[/yellow]")
        return
        
    table = Table(title=table_title)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="bold green", max_width=30)
    table.add_column("Status", style="cyan")
    table.add_column("Priority", style="magenta")
    table.add_column("Due Date", style="yellow")
    
    for task in tasks:
        # --- Add color-coding for priority ---
        priority_style = "green"
        if task['priority'] == 1:
            priority_style = "bold red"
        elif task['priority'] == 2:
            priority_style = "yellow"
        # --- END ---

        table.add_row(
            str(task['id']),
            task['title'],
            task['status'],
            f"[{priority_style}]{task['priority']}[/{priority_style}]", 
            task['due_date'] or ""
        )
    console.print(table)

def handle_add_note():
    """Guides user through adding a new note."""
    console.print("[cyan]Enter note content. (Press Enter twice to save)[/cyan]")
    content_lines = []
    try:
        while True:
            line = input()
            if not line:
                break
            content_lines.append(line)
    except EOFError:
        pass
    
    content = "\n".join(content_lines)
    if not content:
        console.print("[red]Note canceled.[/red]")
        return
        
    # --- UPDATED: Replaced Prompt.ask with input() ---
    tags = input("Tags (comma-separated) (optional): ")
    # --- END UPDATE ---
    Note_Management_Logic.add_note_and_embed(content, tags or None)

def handle_find_similar():
    """Asks for a query and performs semantic search."""
    # --- UPDATED: Replaced Prompt.ask with input() ---
    query = input("What are you looking for?: ")
    # --- END UPDATE ---
    if not query:
        return
        
    console.print(f"[yellow]Searching for notes similar to '{query}'...[/yellow]")
    notes = Note_Management_Logic.find_similar_notes(query)
    
    if not notes:
        console.print("[yellow]No similar notes found.[/yellow]")
        return
        
    table = Table(title="Similar Notes")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Score", style="magenta", width=10)
    table.add_column("Content Snippet", style="green")
    
    for note in notes:
        snippet = note['content'].replace("\n", " ")[:100] + "..."
        table.add_row(
            str(note['id']),
            f"{note['score']:.4f}",
            snippet
        )
    console.print(table)

def handle_find_tag(command):
    """Finds notes by a specific tag."""
    try:
        tag = command.split(" ", 2)[2]
        notes = Note_Management_Logic.find_notes_by_tag(tag)
        if not notes:
            console.print(f"[yellow]No notes found with tag '{tag}'.[/yellow]")
            return
            
        console.print(f"\n[bold cyan]Notes tagged '{tag}':[/bold cyan]")
        for note in notes:
            console.print(f"  [dim]ID {note['id']}:[/dim] {note['content'][:80]}...")
            
    except IndexError:
        console.print("[red]Error: Please provide a tag. (e.g., find tag python)[/red]")

def handle_get_note(command):
    """Gets a single note by ID and prints it."""
    try:
        note_id = command.split(" ")[2]
        note = Note_Management_Logic.get_note_by_id(int(note_id))
        if not note:
            console.print(f"[red]Error: No note found with ID {note_id}[/red]")
        else:
            console.print(f"\n[bold cyan]Note {note['id']}[/bold cyan] [dim]({note['tags']})[/dim]")
            console.print("---")
            console.print(note['content'])
            console.print("---")
            
    except (IndexError, ValueError):
        console.print("[red]Error: Please provide a valid ID. (e.g., get note 5)[/red]")

def handle_summarize_note(command):
    """Gets a note ID, summarizes it, and prints the result in a panel."""
    try:
        note_id = int(command.split(" ")[2])
        console.print(f"[yellow]Generating summary for note {note_id}...[/yellow]")
        
        summary = Note_Management_Logic.summarize_note(note_id)
        
        # Display the summary in a nice panel
        console.print(Panel(
            summary,
            title=f"Summary for Note {note_id}",
            title_align="left",
            border_style="green"
        ))
            
    except (IndexError, ValueError):
        console.print("[red]Error: Please provide a valid ID. (e.g., summarize note 5)[/red]")

def handle_brief_me():
    """
    Calls the AI agent to get a daily briefing and prints it.
    """
    console.print("[yellow]Generating your daily briefing...[/yellow]")
    
    # This function handles all the logic and AI calls
    briefing = ai_agents.get_daily_briefing()
    
    console.print(Panel(
        briefing,
        title="Your Daily Briefing",
        title_align="left",
        border_style="cyan"
    ))

def main_loop():
    """The main chat loop for the application."""
    console.print("[bold green]Welcome to your Personal AI Assistant![/bold green]")
    print_help()
    
    if Note_Management_Logic.CLIENT is None:
        console.print("\n[bold red]Warning: OPENAI_API_KEY is not set.[/bold red]")
        console.print("[yellow]Note-related features (add note, find similar) will not work.[/yellow]")

    while True:
        try:
            # --- UPDATED: Replaced Prompt.ask with input() ---
            command = input("\n> ").lower().strip()
            # --- END UPDATE ---
            
            if not command:
                continue
            
            # --- General Commands ---
            if command == "exit":
                console.print("[bold red]Goodbye![/bold red]")
                break
            elif command == "help":
                print_help()
            elif command == "brief me":
                handle_brief_me()
            
            # --- Task Commands ---
            elif command.startswith("smart add "):
                handle_smart_add(command)
            elif command == "add task detailed":
                handle_add_task()
            elif command.startswith("list tasks"): # --- THIS IS THE FIX ---
                handle_list_tasks(command)           # It now passes 'command'
            elif command.startswith("done "):
                try:
                    task_id = int(command.split(" ")[1])
                    Task_Management_Logic.update_task_status(task_id, "done")
                except (IndexError, ValueError):
                    console.print("[red]Invalid command. Use: done [ID][/red]")
            elif command.startswith("del task "):
                try:
                    task_id = int(command.split(" ")[2])
                    Task_Management_Logic.delete_task(task_id)
                except (IndexError, ValueError):
                    console.print("[red]Invalid command. Use: del task [ID][/red]")
            
            # --- Note Commands ---
            elif command == "add note":
                handle_add_note()
            elif command == "find similar":
                handle_find_similar()
            elif command.startswith("find tag "):
                handle_find_tag(command)
            elif command.startswith("get note "):
                handle_get_note(command)
            elif command.startswith("summarize note "):
                handle_summarize_note(command)
            
            # --- Unknown Command ---
            else:
                console.print("[red]Unknown command. Type 'help' for options.[/red]")
                
        except KeyboardInterrupt:
            # Allow quitting with Ctrl+C
            console.print("\n[bold red]Goodbye![/bold red]")
            break
        except Exception as e:
            # Catch other errors
            console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

if __name__ == "__main__":
    # This is the entry point.
    # First, make sure the database and tables exist.
    Database_initializer.initialize_database()
    
    # Then, start the main application loop.
    main_loop()