# Development Summary: AI-Powered PKMS

Overall Summary of the project seperated by sections of how the project went. I had a lot of fun with the project and learned especially how terminals are vital parts of coding. Through the first few weeks, I was confused on the actual final deliverable that needed to be given for the final project to count in a way, but also needed to find out what I even wanted to do once that realization hit. Those task homework assignments really were the bread and butter for what made this entire thing possible. The use of AI in this class was also another life-saver in helping me close the knowledge gaps that I was having, while also using them to 

## Development Process and AI-Assistance

My development process was highly iterative and conversational, centered around a "dialogue" with my AI assistant. I used the AI in several distinct modes: as an architect, a pair-programmer, a tutor, and a technical support specialist. Majority of the work was done with these assistants for debugging issues on back-end software installs, while also helping structure my code. The only two AI assistants that I used for the entire class was:
Google Gemini PRO
Copilot Pro from Github.
Both of these were provided at the beginning of the class as mandatory installs, whether the other students picked the one I did or not.

### Phase 1: Planning and Architecture

I began with the project's broad requirements. My first step was to use the AI chat service as an AI Architect to format the entire project and bounce ideas from. I presented the requirements to it, and the AI helped me brainstorm the core architecture, breaking the project down into four layers: Storage, Logic, AI, and Interface. We collaboratively debated the pros and cons of using JSON, Neo4J, or SQLite as the storage layer. We decided on SQLite because it is powerful, portable, and doesn't require a separate server or complex file management. This decision worked very well towards the end of the project as there weren't any hiccups from the start using this format. And since it was listed as a storage type, I presumed that it was allowed to be used. The AI then provided an initial "study plan" and prototype stubs for the database to begin working on the project itself.

### Phase 2: Core Logic Prototyping

Once the architecture was set, I used the AI as a Pair-Programmer and Tutor. I asked the AI for the code to build the core database and task management functions, and it generated the initial Database Initializer and Task Manager logic files for me to begin working on. Wovening these two to synchronize with eachother did wonders for me while working on it. When I was confused about a concept, like why the cursor function was needed for these functions to work, It managed to provide an excellent explanation on the topic and make sure I understood it completely from top to bottom, helping me in moving forward with the project.

### Phase 3: The "Smart Librarian" (Where the majority of bugs occured)

The "Smart Librarian" was the most complex feature and involved several pivots. My AI assistant initially suggested using sentence-transformers, a local, open-source model for creating embeddings. This was a false start because it required a heavy installation called torch, something I have never heard of in my lifetime and would be uncomfortable with using, and it never was mentioned in the lectures at all. To address my concern about heavy installs, I asked if it was possible to build it without any new libraries. The AI explained that this was not possible for true AI search but provided a non-AI "Keyword Librarian" using SQL LIKE. This was a second false start, as it met the "no-install" constraint but failed the "AI agent" project requirement.

The breakthrough came when I asked, "Can't I just use OpenAI from my lecture?" The AI immediately pivoted, explaining the trade-offs (cloud vs. local, cost vs. free) and generated a new prototype, note_manager.py, using the openai library for embeddings. This was a much better solution, as it was lightweight and re-used the same openai library we would need for other agents.

With that, it assetted with a new mountain of debugging to make it work properly, sometimes the list tasks function wouldn't know where it was, while other times the AI didn't know any key was used for it. In the end, I asked 

###  Phase 4: Iterative Feature Development & Workflow

With the core logic in place, I asked the AI to adopt a professional workflow. I would check in with it to make improvements on the changtes that I made, making sure it let me know if the changes were actually good or harmful. I also asked for it to provide me a direction to take these improvements in the case I didn't have any ideas. This was extremely effective. From this point on, every new feature was added as a logical, well-documented change. With the help of AI, I rapidly built all the key AI agents, one by one. For the AI note summarizer, Google Gemini knew to fetch the note from Note_Manager_Logic file and use the Chat Completions API. For the 'smart add' agent, Copilot steered me in the right direction to write a function using a detailed system prompt and OpenAI's "JSON mode" to parse natural language into a structured task. For the 'Daily Briefing', Google Gemini created a new ai_agents file to house the agent, which fetches tasks and uses an LLM to write a prioritized, friendly summary.

### Phase 5: Final Setup and Finishing Touches

Finally, I used the AI as a Technical Support Specialist when back-end issues arose. One main example I used it for was when the packages that were suggested needed more specific installs, so I asked Gemini to assist me in that process before more testing commenced as both of the packages had been updated compared to when I used them in the past. With those confusions out of the way, I would run the last set of tests before being satisfied with the final product I am providing for the final project, along with some final touches to the bug fixes that needed to be addressed. All of the packages I used were just add-ons with quick installs with cosmetic intent, with 95% of the project still being OpenAI operated.
# ----------------------------------------------------------------------------------------------------
This conversational way of talking to the AI assistant (Architect, Tutor, Pair-Programmer) chat service was the cornerstone of my development process and managed to help me get to where I am now. With that, I hope you find it a little fun to run the final project I created (Even with its very simple a boring menu, I tried to make it a little colorful).