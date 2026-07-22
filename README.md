# ClickUp RAG Agent (ClickUp Time Dashboard Suite)

## The Problem

ClickUp tracks everything. That's the issue. By the time a business leader wants to know something simple, who's over capacity this month, where are our estimates consistently wrong, how much of last week was actually billable, the answer is buried across hundreds of tasks, time entries, and custom fields. Native reporting shows you hours logged. It doesn't let you ask.

So you export to a spreadsheet, you filter, you pivot, you reconcile. The question doesn't change week to week. The lag in answering it is where the real cost lives.

This project removes the lag. You ask. It answers.

---

## What This Does

The ClickUp RAG Agent is an advanced Python application and conversational interface built on top of the **[ClickUp Time Dashboard](https://github.com/bstcyr229/clickup-time-dashboard)** ecosystem. It pulls your workspace's time-tracking data, structures it for deep analysis, and lets you query it conversationally.

Instead of clicking through reports, you type:
- "Which team members logged the most non-billable hours last month?"
- "Show me tasks where actual hours blew past the estimate."
- "How much billable time did the design team produce?"

The agent retrieves the relevant task records from a vector store, hands them to the model as context, and responds with an answer drawn directly from your workspace data — not a guess.

---

## The Foundation: What the ClickUp Time Dashboard Does

Before powering the conversational AI layer, the underlying **[ClickUp Time Dashboard](https://github.com/bstcyr229/clickup-time-dashboard)** module solves the heavy lifting of raw data extraction and operational modeling. 

For recruiters and technical evaluators, the core dashboard script performs the following critical functions:

* **Automated API Extraction:** Connects directly to the ClickUp API to securely fetch workspace-wide time entries, tasks, assignees, custom fields, and hierarchical project structures.
* **Data Cleansing & Normalization:** Flattens nested JSON payloads into clean, structured **pandas DataFrames** designed for robust analysis.
* **Operational Intelligence Metrics:** 
  * Calculates billable versus non-billable utilization rates per team member and department.
  * Tracks variance metrics comparing estimated project hours against actual time spent.
  * Aggregates throughput and capacity trends across custom date ranges.
* **Modular Architecture:** Built as a standalone, reusable module (`dashboard.py`) so downstream applications (like this RAG agent) can import core data pipelines without duplicating API calls or business logic.

---

## How It Works

This project is the third step in a structured build, leveraging the core data pipeline established in the **[ClickUp Time Dashboard](https://github.com/bstcyr229/clickup-time-dashboard)**:

1. **Data layer (reused).** The existing ClickUp Time Intelligence Dashboard module is imported directly. Its functions handle API authentication, data fetching, and pandas DataFrame shaping (assignees, tasks, billable flags, estimates, and due dates). 
2. **Ingestion.** Each structured task row is flattened into a concise natural-language document and embedded using Google Gemini. The embeddings, documents, and IDs are stored in a local ChromaDB collection that persists to disk.
3. **Retrieval + generation.** When you submit a prompt, the agent embeds the query, retrieves the most relevant task records out of ChromaDB, and passes them to the model as grounding context. Responses are directly traceable to the underlying source records.
4. **Interface.** A Streamlit front end turns the pipeline into a responsive, production-ready chat interface.

---

## Tech Stack

| Layer | Tool |
| :--- | :--- |
| **Language** | Python 3.11 |
| **Vector store** | ChromaDB (`PersistentClient`) |
| **Embeddings** | Google Gemini (`google-genai`) |
| **Data shaping** | pandas |
| **Source data** | ClickUp API (via the imported [ClickUp Time Dashboard](https://github.com/bstcyr229/clickup-time-dashboard) module) |
| **Interface** | Streamlit |
| **Config** | python-dotenv |

---

## Getting Started

### Prerequisites
- Python 3.11
- A ClickUp API token
- A Google Gemini API key

### Setup

```bash
# Clone the repo
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
```

### Environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_key_here
CLICKUP_API_TOKEN=your_clickup_token_here
```

*A note from hard experience: confirm your editor is pointing at the project's `.venv` before you run anything. A mismatched interpreter is responsible for more "impossible" bugs than any actual code.*

---

## Run it

```bash
# Ingest your ClickUp data into the vector store (run once, or after data changes)
python ingest.py

# Launch the chat interface
streamlit run app.py
```

---

## Project Structure

```text
clickup-rag-agent/
├── app.py              # Streamlit chat interface + retrieval/generation
├── ingest.py           # Pulls ClickUp data, embeds it, writes to ChromaDB
├── dashboard.py        # Imported module from the ClickUp Time Dashboard (ClickUp API + pandas shaping)
├── chroma_db/          # Persisted vector store (gitignored)
├── .env                # API keys (gitignored)
├── requirements.txt
└── README.md
```

---

## Status

This is an active build. The ingestion pipeline and the conversational query layer are the current focus — getting clean task documents into ChromaDB with the correct Gemini embedding configuration, then wiring `collection.query()` into the chat flow.

### Working
- ClickUp data retrieval and DataFrame shaping (via the imported [ClickUp Time Dashboard](https://github.com/bstcyr229/clickup-time-dashboard) module)
- Persistent ChromaDB collection

### In progress
- Gemini embedding function wired correctly into ingestion
- `collection.query()` connected to the Streamlit chat interface
- End-to-end conversational querying

---

## Why I'm Building This

I spent years inside ClickUp on the operations side, watching teams ask the same business questions and never get clean answers fast enough. I'm building the tool I always wanted to hand them — and learning to build production AI systems in the process. This repo is part of a public, documented learning path from operations into AI development, seamlessly extending the **[ClickUp Time Dashboard](https://github.com/bstcyr229/clickup-time-dashboard)** suite.

If you're a recruiter, a fellow self-taught developer, or someone who just got tired of exporting ClickUp data to spreadsheets — you're in the right place.

---

## License

MIT
