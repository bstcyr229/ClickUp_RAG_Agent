The Problem

ClickUp tracks everything. That's the issue. By the time a business leader wants to know something simple, who's over capacity this month, where are our estimates consistently wrong, how much of last week was actually billable — the answer is buried across hundreds of tasks, time entries, and custom fields. Native reporting shows you hours logged. It doesn't let you ask.

So you export to a spreadsheet, you filter, you pivot, you reconcile. The question doesn't change week to week. The lag in answering it is where the real cost lives.

This project removes the lag. You ask. It answers.

What This Does

The ClickUp RAG Agent is a Python application that pulls your workspace's time-tracking data, turns it into something a language model can reason over, and lets you query it conversationally.

Instead of clicking through reports, you type:


"Which team members logged the most non-billable hours last month?"
"Show me tasks where actual hours blew past the estimate."
"How much billable time did the design team produce?"



The agent retrieves the relevant task records from a vector store, hands them to the model as context, and responds with an answer drawn from your data — not a guess.

How It Works

This is the third project in a sequence, and it deliberately builds on the second one rather than starting over.


Data layer (reused). The existing ClickUp Time Intelligence Dashboard is imported as a module. Its functions handle the ClickUp API calls and shape the raw response into a clean pandas DataFrame — team member, task, billable vs. non-billable hours, estimates, due dates, and so on. Collect first, structure second. That work was already solved, so the RAG agent imports it instead of duplicating it.
Ingestion. Each task row is flattened into a short natural-language document and embedded using Google Gemini. The embeddings, documents, and IDs are stored in a local ChromaDB collection that persists to disk.
Retrieval + generation. When you ask a question, the agent embeds the query, pulls the most relevant task records out of ChromaDB, and passes them to the model as grounding context. The answer comes back tied to the records that produced it.
Interface. A Streamlit front end turns the whole thing into a chat window you can actually demo.


Tech Stack

LayerToolLanguagePython 3.11Vector storeChromaDB (PersistentClient)EmbeddingsGoogle Gemini (google-genai)Data shapingpandasSource dataClickUp API (via the Time Intelligence Dashboard module)InterfaceStreamlitConfigpython-dotenv

Getting Started

Prerequisites


Python 3.11
A ClickUp API token
A Google Gemini API key


Setup

bash# Clone the repo
git clone https://github.com/bstcyr229/clickup-rag-agent.git
cd clickup-rag-agent

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

Environment variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_key_here
CLICKUP_API_TOKEN=your_clickup_token_here


A note from hard experience: confirm your editor is pointing at the project's .venv before you run anything. A mismatched interpreter is responsible for more "impossible" bugs than any actual code.



Run it

bash# Ingest your ClickUp data into the vector store (run once, or after data changes)
python ingest.py

# Launch the chat interface
streamlit run app.py

Project Structure

clickup-rag-agent/
├── app.py            # Streamlit chat interface + retrieval/generation
├── ingest.py         # Pulls ClickUp data, embeds it, writes to ChromaDB
├── dashboard.py      # Imported module from Project 2 (ClickUp API + pandas shaping)
├── chroma_db/        # Persisted vector store (gitignored)
├── .env              # API keys (gitignored)
├── requirements.txt
└── README.md

Status

This is an active build. The ingestion pipeline and the conversational query layer are the current focus — getting clean task documents into ChromaDB with the correct Gemini embedding configuration, then wiring collection.query() into the chat flow.

Working


ClickUp data retrieval and DataFrame shaping (via the imported dashboard module)
Persistent ChromaDB collection


In progress


Gemini embedding function wired correctly into ingestion
collection.query() connected to the Streamlit chat interface
End-to-end conversational querying


Why I'm Building This

I spent years inside ClickUp on the operations side, watching teams ask the same business questions and never get clean answers fast enough. I'm building the tool I always wanted to hand them — and learning to build production AI systems in the process. This repo is part of a public, documented learning path from operations into AI development.

If you're a recruiter, a fellow self-taught developer, or someone who just got tired of exporting ClickUp data to spreadsheets — you're in the right place.

License

MIT
=======
README
>>>>>>> master
