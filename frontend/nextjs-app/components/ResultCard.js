// frontend/nextjs-app/components/ResultCard.js
export default function ResultCard({ r, onFeedback }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h3 style={{ margin: 0 }}>{r.title}</h3>
        <div style={{ color: "#666" }}>{r.score.toFixed(3)}</div>
      </div>
      <p style={{ color: "#333" }}>{r.body?.slice(0, 250)}</p>
      {r.source_url && <a href={r.source_url} target="_blank" rel="noreferrer">View source</a>}
      <div style={{ marginTop: 8 }}>
        <button onClick={() => onFeedback(r.id, true)} style={{ marginRight: 8 }}>Useful</button>
        <button onClick={() => onFeedback(r.id, false)}>Not useful</button>
      </div>
    </div>
  );
}
