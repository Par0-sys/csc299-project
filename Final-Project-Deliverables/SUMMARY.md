Development Summary: AI-Powered PKMS

This document details the development process for my AI-powered Personal Knowledge Management System (PKMS) and Task Manager. The project's goal was to create a portable, terminal-based application in Python that integrates AI agents to manage notes and tasks. The primary development partner for this project was a chat-based AI assistant (Gemini).

Development Process and AI-Assistance

My development process was highly iterative and conversational, centered around a "dialogue" with my AI assistant. I used the AI in several distinct modes: as an architect, a pair-programmer, a tutor, and a technical support specialist. Majority of the work was done with Google Gemini with the help of Copilot for debugging issues on back-end software installs.

Phase 1: Planning and Architecture

I began with the project's broad requirements. My first step was to use the AI chat service as an AI Architect. I presented the requirements, and the AI helped me brainstorm the core architecture, breaking the project down into four layers: Storage, Logic, AI, and Interface. We collaboratively debated the pros and cons of using JSON, Neo4J, or SQLite as the storage layer. We decided on SQLite because it is powerful, portable, and doesn't require a separate server or complex file management. This was a critical decision that worked very well. The AI then provided an initial "study plan" and prototype stubs for the database.

Phase 2: Core Logic Prototyping

Once the architecture was set, I used the AI as a Pair-Programmer and Tutor. I asked the AI for the code to build the core database and task management functions, and it generated the initial database.py and task_manager.py files. When I was confused about a concept, such as "Why is cursor used?", I used the AI as a tutor to get a clear, concise explanation. This was highly effective. I had functional, well-commented code for my core CRUD (Create, Read, Update, Delete) operations in minutes, which allowed me to focus on the more complex AI features.

Phase 3: The "Smart Librarian" (A Case Study in Pivots)

The "Smart Librarian" was the most complex feature and involved several pivots. My AI assistant initially suggested using sentence-transformers, a local, open-source model for creating embeddings. This was a false start because it required a heavy installation (torch). To address my concern about heavy installs, I asked if it was possible to build it without any new libraries. The AI explained that this was not possible for true AI search but provided a non-AI "Keyword Librarian" using SQL LIKE. This was a second false start, as it met the "no-install" constraint but failed the "AI agent" project requirement.

The breakthrough came when I asked, "Can't I just use OpenAI?" The AI immediately pivoted, explaining the trade-offs (cloud vs. local, cost vs. free) and generated a new prototype, note_manager.py, using the openai library for embeddings. This was a much better solution, as it was lightweight and re-used the same openai library we would need for other agents.

Phase 4: Iterative Feature Development & Workflow

With the core logic in place, I asked the AI to adopt a professional workflow. I instructed it: "make improvements to the code... also have a commit message to follow." This was extremely effective. From this point on, every new feature was added as a logical, well-documented change. We rapidly built all the key AI agents, one by one. For the AI note summarizer, the AI knew to fetch the note from note_manager.py and use the Chat Completions API. For the 'smart add' agent, the AI wrote a function using a detailed system prompt and OpenAI's "JSON mode" to parse natural language into a structured task. For the 'Daily Briefing', the AI created a new ai_agents.py file to house the agent, which fetches tasks and uses an LLM to write a prioritized, friendly summary.

Phase 5: Final Setup and Deployment

Finally, I used the AI as a Technical Support Specialist when back-end issues arose. One main example I used it for was when the packages that were suggested needed more specific installs, so I asked Gemini to assist me in that process before more testing commenced. With those confusions out of the way, I would run the last set of tests before being satisfied with the final product I am providing for the final project.

This conversational, iterative, and "persona-driven" (Architect, Tutor, Pair-Programmer) use of an AI chat service was the cornerstone of my development process.