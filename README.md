# DicoVR: AI Product Discovery System

A production-quality full-stack application built for a technical hiring assessment. It allows users to browse a product catalog and discover products using natural language queries powered by a local LLM (Ollama).

## Tech Stack
- **Frontend:** React 18, Vite, Fetch API, Vanilla CSS.
- **Backend:** Python 3.11+, FastAPI, Pydantic, HTTPX.
- **AI:** Ollama (Local model via HTTP API).

## Project Structure
```text
backend/
  app/
    data/products.json      # Product catalog (JSON database)
    services/
      retrieval_service.py  # Keyword scoring & RAG retrieval
      llm_service.py        # Ollama API communication
    config.py               # Settings and Env management
    models.py               # Pydantic schemas
    routes.py               # API endpoints
    main.py                 # FastAPI initialization
  .env                      # Environment variables
  requirements.txt          # Python dependencies

frontend/
  src/
    components/             # Reusable UI components
    api.js                  # API communication layer
    App.jsx                 # Core logic & state management
  package.json              # Node dependencies
```

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.com/) installed and running.

### 2. AI Configuration (Ollama)
1️⃣ Install Ollama

Download and install from:

👉 https://ollama.com/

After installation, verify:

ollama --version
2️⃣ Pull the Model

Use a lightweight model:

ollama pull gemma3:1b

(Recommended because it’s small and fast.)

3️⃣ Start Ollama Server

Ollama automatically runs on:

http://localhost:11434

Verify:

curl http://localhost:11434
4️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Run backend:

uvicorn app.main:app --reload

⚠️ Note: Ollama must be installed and running locally before starting the backend.
If the LLM service is unavailable, the backend will return a 502 error.
### 3. Backend Setup
1. Navigate to `backend/`.
2. Setup environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and adjust if necessary.
4. Run the backend:
   ```bash
   python -m app.main
   ```

### 4. Frontend Setup
1. Navigate to `frontend/`.
2. Install and run:
   ```bash
   npm install
   npm run dev
   ```

## Example API Usage
```bash
# Get Products
curl http://localhost:8000/api/products

# Ask AI
curl -X POST http://localhost:8000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "best laptop for gaming"}'
```

## Retrieval Logic (RAG)
1. **Keyword Scoring:** Matches query tokens against product names, categories, descriptions, and tags.
2. **Filtering:** Supports strict price detection (e.g., "under 1000").
3. **LLM Synthesis:** Sends the top 3 relevant items to the LLM for a final recommendation summary.

## Time Spent
- Backend (FastAPI + RAG): 45 mins
- Frontend Integration: 20 mins
- Debugging & Refinement: 25 mins
- Documentation: 10 mins
- **Total: ~100 minutes**
