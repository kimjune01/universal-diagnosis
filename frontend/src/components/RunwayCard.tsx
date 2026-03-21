import { Financials } from "../types";

interface Props {
  financials: Financials | null;
}

export function RunwayCard({ financials }: Props) {
  if (!financials) return null;

  const { cash, quarterly_burn, runway_quarters, runway_months, source_date } = financials;
  const cashM = (cash / 1_000_000).toFixed(0);
  const burnM = (quarterly_burn / 1_000_000).toFixed(0);

  const maxQ = 20;
  const pct = runway_quarters ? Math.min((runway_quarters / maxQ) * 100, 100) : 0;
  const barColor = (runway_quarters || 0) > 8 ? "#4ade80" : (runway_quarters || 0) > 4 ? "#fbbf24" : "#f87171";

  return (
    <div style={{ background: "#141414", border: "1px solid #222", borderRadius: 8, padding: 12, fontSize: "0.78rem", fontFamily: "monospace" }}>
      <div style={{ color: "#555", fontSize: "0.65rem", letterSpacing: "0.1em", marginBottom: 6 }}>RUNWAY</div>
      <div style={{ color: "#888", marginBottom: 6 }}>
        Cash: <span style={{ color: "#e0e0e0" }}>${cashM}M</span>
        {"  "}Burn: <span style={{ color: "#e0e0e0" }}>${burnM}M/q</span>
        {"  "}
        {runway_quarters && (
          <span style={{ color: barColor, fontWeight: "bold" }}>{runway_quarters}q</span>
        )}
      </div>
      <div style={{ height: 6, background: "#222", borderRadius: 3, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${pct}%`, background: barColor, borderRadius: 3, transition: "width 0.3s" }} />
      </div>
      <div style={{ color: "#444", fontSize: "0.65rem", marginTop: 4 }}>as of {source_date}</div>
    </div>
  );
}
