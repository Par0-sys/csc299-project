import os
from openai import OpenAI

# 1. Setup the OpenAI client
# It automatically looks for the OPENAI_API_KEY environment variable.
client = OpenAI()

# 2. Define sample paragraph-length tasks
sample_tasks = [
    """
    I need to refactor the user authentication module in our web application. 
    Currently, it's using an outdated hashing algorithm and the session management 
    is buggy, leading to random logouts for users on mobile devices. The new 
    implementation should use Argon2 for hashing and JWTs for session management, 
    ensuring robust security and a smoother user experience across all platforms.
    """,
    """
    For the upcoming weekend gardening project, I have to clear out the 
    overgrown weeds in the backyard, specifically around the tomato patch. 
    After weeding, I need to till the soil and mix in the new compost I bought 
    yesterday. Finally, I need to plant the new rows of marigolds to act as 
    a natural pest repellent for the vegetables.
    """
]

def summarize_task(task_description):
    """Sends a task description to OpenAI for a short phrase summary."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Swapped to standard current mini model
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant. Summarize the following task description into a single short phrase."
            },
            {"role": "user", "content": task_description}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# 3. Loop through tasks independently and print summaries
def main():
    print("Starting task summarization experiment...\n")
    
    for i, task in enumerate(sample_tasks, 1):
        print(f"--- Processing Task {i} ---")
        summary = summarize_task(task)
        print(f"Original (len): {len(task.strip())} chars")
        print(f"Summary: {summary}\n")

if __name__ == "__main__":
    main()