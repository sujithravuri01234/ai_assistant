# Agentic AI Assistant

A full-stack AI assistant for multi-department support (HR, IT Support, Customer Support, Product & Promotions) with:
- Query routing by sentiment + department
- RAG from ChromaDB knowledge base
- AI waterfall cascade fallback (2 to 3 model steps)
- Human escalation workflow when needed
- React frontend with runtime light/dark theme switching

## Project Structure

```text
Agentic-AI-Assistant-main/
+- agents/                 # router, rag, escalation agents
+- app/                    # FastAPI backend
+- graph/                  # LangGraph orchestration
+- data/                   # department Q&A data files
+- vector_store/           # Chroma persisted embeddings
+- frontend/               # React + Vite frontend
+- requirements.txt        # backend dependencies
+- README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- A valid `GROQ_API_KEY`

## Environment Setup

1. Create/update `.env` in project root:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional: comma-separated waterfall model list (max first 3 used)
GROQ_CASCADE_MODELS=llama-3.3-70b-versatile,llama-3.1-8b-instant,mixtral-8x7b-32768

# Optional embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Backend Setup (FastAPI)

From project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run backend server separately:

```powershell
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

Backend URLs:
- API root: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

## Frontend Setup (React + Vite)

From `frontend` directory:

```powershell
cd Agentic-AI-Assistant-main
cd frontend
npm install
```

Run frontend server separately:

```powershell
npm run dev -- --host 0.0.0.0 --port 5173
```

Frontend URL:
- App: `http://localhost:5173`

## Running Frontend and Backend Together

Use 2 terminals.

Terminal 1 (project root):
```powershell
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 (`frontend` folder):
```powershell
npm run dev -- --host 0.0.0.0 --port 5173
```

## How It Works

1. Router agent classifies user query into sentiment + department.
2. If sentiment is negative, escalation agent handles it.
3. Otherwise RAG agent answers:
   - department retrieval from ChromaDB
   - cross-department retrieval fallback
   - waterfall AI cascade fallback if KB is insufficient
4. Frontend chat UI renders answer and optional escalation form.

## Current Frontend Features

- First-load theme chooser (light/dark)
- In-page theme toggle (switch anytime)
- Improved readable chat composer
- Responsive sidebar + chat layout

## Common Commands

Backend syntax check:

```powershell
python -m py_compile agents/rag_agent.py graph/agent_graph.py agents/router_agent.py app/api.py
```

Frontend production build:

```powershell
cd frontend
npm run build
```

## Troubleshooting

- If backend fails with auth errors: verify `GROQ_API_KEY` in `.env`.
- If frontend cannot fetch backend: ensure backend is running on port `8000`.
- If PowerShell blocks npm scripts: use `npm.cmd` instead of `npm`.
- If RAG gives weak answers: verify `vector_store` exists and data ingestion was completed.

## Notes

- `frontend/node_modules` contains third-party README files; do not edit/remove those.
- This README replaces both old project readmes (`README.md` and `frontend/README.md`).
