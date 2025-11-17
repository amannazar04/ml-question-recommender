# 📘 Similar Questions Recommender (ML + FastAPI + FAISS + MongoDB + Next.js)

A production‑ready **semantic search engine** that finds similar questions using:

* 🧠 **ML embeddings** (Sentence Transformers / MiniLM)
* ⚡ **FAISS** vector similarity search
* 🍃 **MongoDB** for storing question metadata
* 🚀 **FastAPI** backend for search API
* 🌐 **Next.js** elegant frontend with Tailwind + Framer Motion
* 🔌 Fully deployable backend + frontend

This project is ideal for **ML Engineer internships**, showcasing:

* ML model usage in real-world apps
* API development
* Full‑stack integration
* Deployment-ready structure

---

# 🏗️ Architecture Overview

```
User → Next.js UI → FastAPI Search API → FAISS Vector Index → MongoDB Metadata
```

### 🔹 Steps

1. User searches a question.
2. Query gets embedded using the ML model.
3. FAISS finds nearest vectors.
4. MongoDB returns metadata for matched questions.
5. Frontend displays results beautifully.

---

# 🚀 Features

### ✔ Semantic Search (meaning‑based)

### ✔ FAISS vector retrieval

### ✔ MongoDB metadata store

### ✔ CSV dataset ingestion

### ✔ Elegant Next.js UI

### ✔ 100% ready for hosting (Render, Railway, Vercel)

### ✔ Modern animations using Framer Motion

---

# 📂 Folder Structure

```
similar_questions/
│
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── embeddings.py      # Model wrapper
│   │   ├── utils.py           # FAISS loader/saver
│   │   ├── db.py              # MongoDB connection
│   │   ├── models.py          # Pydantic schemas
│   │   ├── scripts/
│   │   │   └── ingest_csv.py  # CSV ingestion tool
│   │   └── faiss_index/       # Generated FAISS files
│   └── requirements.txt
│
├── frontend/
│   └── nextjs-app/
│       ├── app/page.js        # Main UI
│       ├── styles/globals.css
│       ├── package.json
│       └── ...
│
└── dataset/
    └── questions.csv          # Demo dataset
```

---

# 🛠️ Setup Instructions

## 1️⃣ Clone the Repo

```
git clone https://github.com/<your-username>/<your-repo>.git
cd similar_questions
```

---

# 🔧 Backend Setup (FastAPI)

## Create & activate virtual environment

```
cd backend/app
python -m venv venv
venv\Scripts\activate
```

## Install dependencies

```
pip install -r ../requirements.txt
```

## Configure MongoDB

Create a `.env` file:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/hello
```

## Ingest dataset

```
python scripts/ingest_csv.py
```

## Run backend

```
uvicorn main:app --reload --port 8000
```

Backend will be live at:

```
http://127.0.0.1:8000
```

---

# 🎨 Frontend Setup (Next.js)

## Install dependencies

```
cd frontend/nextjs-app
npm install
```

## Add environment variable

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Start frontend

```
npm run dev
```

Site opens at:

```
http://localhost:3000
```

---

# 🧪 Testing API

Using PowerShell:

```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/search" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"query":"python decorators", "k":5}'
```

---

# 🌐 Deployment Guide

## FastAPI Backend → Render / Railway / AWS EC2

### Steps:

1. Push code to GitHub
2. Create a new service in Render/Railway
3. Add environment variable `MONGO_URI`
4. Deploy

## Next.js Frontend → Vercel

1. Import GitHub repo
2. Set env var:

```
NEXT_PUBLIC_API_URL=https://your-backend-url
```

3. Deploy

---

# 📊 Future Enhancements

* Add search history
* Add filters by tags
* Add user feedback reinforcement
* Add RAG or LLM-powered ranking
* Add enhanced analytics dashboard

---

# 📜 License

MIT License

---

# 🙌 Author

**Aman Nazar**

If you want me to generate a portfolio page or a project walkthrough video script, just ask!
