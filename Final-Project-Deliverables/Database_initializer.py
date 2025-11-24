import sqlite3
from pathlib import Path

# This will create 'my_system.db' in the same folder as your scripts
DB_FILE = Path(__file__).parent / "my_system.db"

def initialize_database():
    """
    Creates the database and tables if they don't exist.
    This is safe to run multiple times.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # --- Create Tasks Table ---
    # status: 'todo', 'doing', 'done'
    # priority: 1 (High), 2 (Medium), 3 (Low)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'todo',
        priority INTEGER DEFAULT 3,
        due_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # --- Create Notes Table ---
    # embedding: A BLOB (raw bytes) to store the vector
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        tags TEXT,
        embedding BLOB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    print(f"Database initialized at {DB_FILE}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()