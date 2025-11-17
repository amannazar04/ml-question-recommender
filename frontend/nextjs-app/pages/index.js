// frontend/nextjs-app/pages/index.js
import { useState } from "react";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  async function handleSearch(e) {
    e.preventDefault();
    if (!q.trim()) return;
    setLoading(true);
    const res = await fetch(`${API_URL}/search`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ query: q, k: 5 })
    });
    const data = await res.json();
    setResults(data.results || []);
    setLoading(false);
  }

  async function sendFeedback(id, useful) {
    await fetch(`${API_URL}/feedback`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ question_id: id, useful })
    });
    // Optionally update UI or show toast
  }

  return (
    <div style={{ display: "flex", justifyContent:"center", padding: "40px" }}>
      <div style={{ width: 800 }}>
        <h1>Similar Questions Recommender</h1>
        <form onSubmit={handleSearch} style={{ display: "flex", marginBottom: 20 }}>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Type your question..."
            style={{ flex: 1, padding: "10px", fontSize: 16 }}
          />
          <button type="submit" style={{ marginLeft: 10, padding: "10px 18px" }}>
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        <div>
          {results.length === 0 && !loading && <p>No results yet. Try a sample query like "reverse linked list".</p>}
          {results.map((r) => (
            <ResultCard key={r.id} r={r} onFeedback={sendFeedback} />
          ))}
        </div>
      </div>
    </div>
  );
}
