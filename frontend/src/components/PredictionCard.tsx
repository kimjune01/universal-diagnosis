import { Prediction, Analyst, STATUS_COLORS } from "../types";

interface Props {
  prediction: Prediction | null;
  analyst: Analyst | null;
}

export function PredictionCard({ prediction, analyst }: Props) {
  if (!prediction) return null;

  const dirColor = prediction.direction === "pass" ? "#4ade80" : "#f87171";
  const outcomeColor =
    prediction.outcome === "hit" ? "#4ade80" : prediction.outcome === "miss" ? "#f87171" : "#666";

  const daysLeft = Math.ceil(
    (new Date(prediction.window_end).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
  );

  return (
    <div style={{ background: "#141414", border: "1px solid #222", borderRadius: 8, padding: 12, fontSize: "0.78rem", fontFamily: "monospace" }}>
      <div style={{ marginBottom: 8 }}>
        <span style={{ color: dirColor, fontWeight: "bold" }}>
          {prediction.direction.toUpperCase()}
        </span>
        <span style={{ color: "#555" }}> ({prediction.category?.replace("_", " ")})</span>
      </div>

      <div style={{ color: "#888", marginBottom: 4 }}>
        <strong style={{ color: "#aaa" }}>Catalyst:</strong> {prediction.catalyst}
      </div>
      <div style={{ color: "#888", marginBottom: 4 }}>
        <strong style={{ color: "#aaa" }}>Window:</strong> {prediction.window_start} → {prediction.window_end}
        {daysLeft > 0 && <span style={{ color: "#555" }}> ({daysLeft}d left)</span>}
      </div>
      <div style={{ color: "#888", marginBottom: 4 }}>
        <strong style={{ color: "#aaa" }}>Pass condition:</strong> {prediction.pass_condition}
      </div>
      <div style={{ color: outcomeColor, fontWeight: "bold", marginBottom: 8 }}>
        Outcome: {prediction.outcome?.toUpperCase() || "PENDING"}
      </div>

      {analyst && (
        <div style={{ borderTop: "1px solid #222", paddingTop: 8 }}>
          <div style={{ color: "#888" }}>
            <strong style={{ color: "#aaa" }}>{analyst.analyst_name}</strong>
            {" — "}
            <span style={{ color: analyst.direction === "pass" ? "#4ade80" : "#f87171" }}>
              {analyst.direction.toUpperCase()}
            </span>
          </div>
          {analyst.source_url && (
            <a
              href={analyst.source_url}
              target="_blank"
              rel="noopener"
              style={{ fontSize: "0.65rem", color: "#444" }}
            >
              source ↗
            </a>
          )}
        </div>
      )}
    </div>
  );
}
