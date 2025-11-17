# Similar Questions Recommender

A small web app: ask a question and get similar previously-asked questions.  
Stack: SentenceTransformers + FAISS + FastAPI + MongoDB + Next.js (Vercel).

See `backend/` and `frontend/nextjs-app/` for code.

## Quick local run (backend)
1. Create virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt
