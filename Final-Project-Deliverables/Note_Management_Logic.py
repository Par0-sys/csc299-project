import sqlite3
from pathlib import Path
import pickle  # To serialize/deserialize the numpy array
import numpy as np
from openai import OpenAI
import os

# --- Setup ---
DB_FILE = Path(__file__).parent / "my_system.db"

# Check for API key and initialize client
if "OPENAI_API_KEY" not in os.environ:
    print("="*50)
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set the variable before running the app.")
    print("="*50)
    CLIENT = None
else:
    CLIENT = OpenAI()
    
EMBEDDING_MODEL = "text-embedding-3-small"

def get_embedding_from_api(text):
    """Helper function to call the OpenAI API."""
    if CLIENT is None:
        raise EnvironmentError("OpenAI API key not set.")
    response = CLIENT.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return np.array(response.data[0].embedding)

def add_note_and_embed(content, tags=None):
    """
    Adds a note and its AI-generated embedding to the database.
    """
    try:
        embedding = get_embedding_from_api(content)
        embedding_bytes = pickle.dumps(embedding)  # Serialize array to bytes
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        sql = "INSERT INTO notes (content, tags, embedding) VALUES (?, ?, ?)"
        cursor.execute(sql, (content, tags, embedding_bytes))
        conn.commit()
        conn.close()
        print(f"Added and embedded note: '{content[:30]}...'")
    except Exception as e:
        print(f"Error adding note: {e}")

def find_similar_notes(query_text, top_k=3):
    """
    This is the "Smart Librarian."
    Finds the most semantically similar notes.
    """
    try:
        query_embedding = get_embedding_from_api(query_text)
        
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # This is the "inefficient" part: load all embeddings
        cursor.execute("SELECT id, content, embedding FROM notes")
        all_notes = cursor.fetchall()
        conn.close()
        
        if not all_notes:
            return []
            
        # Deserialize and compare
        db_embeddings = []
        note_data = []
        for note in all_notes:
            db_embeddings.append(pickle.loads(note['embedding']))
            note_data.append(note)
            
        # Cosine similarity calculation
        def cosine_similarity(v1, v2):
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            return dot_product / (norm_v1 * norm_v2)

        scores = []
        for i, emb in enumerate(db_embeddings):
            score = cosine_similarity(query_embedding, emb)
            scores.append((score, i)) # (score, original_index)

        # Sort by score and get top_k
        scores.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, idx in scores[:top_k]:
            results.append({
                "id": note_data[idx]['id'],
                "content": note_data[idx]['content'],
                "score": float(score)
            })
        return results
        
    except Exception as e:
        print(f"Error finding similar notes: {e}")
        return []

def find_notes_by_tag(tag):
    """Finds notes by a simple tag keyword search."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_term = f"%{tag}%"
    sql = "SELECT id, content, tags FROM notes WHERE tags LIKE ?"
    
    cursor.execute(sql, (search_term,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_note_by_id(note_id):
    """Retrieves a single note by its exact ID."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = "SELECT id, content, tags FROM notes WHERE id = ?"
    cursor.execute(sql, (note_id,))
    note = cursor.fetchone()
    conn.close()
    return note

def summarize_note(note_id):
    """
    Summarizes the content of a specific note using an AI chat model.
    """
    # 1. Get the note content from our database
    note = get_note_by_id(note_id)
    if not note:
        return f"Error: No note found with ID {note_id}"
        
    if CLIENT is None:
        return "Error: OpenAI API key not set. Cannot summarize."

    # 2. Prepare the prompt for the AI
    system_prompt = "You are a concise assistant. Summarize the following note into one or two key sentences."
    user_content = note['content']
    
    try:
        # 3. Call the Chat Completions API
        response = CLIENT.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3, # Low temperature for more factual summaries
            max_tokens=100
        )
        
        summary = response.choices[0].message.content
        return summary
        
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error: Failed to get summary from AI."
    