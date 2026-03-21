import type { Event } from "../types";
import { STATUS_COLORS, STATUS_ICONS } from "../types";

interface Props {
  events: Event[];
  selectedId: number | null;
  onSelect: (id: number) => void;
}

export function EventTimeline({ events, selectedId, onSelect }: Props) {
  if (events.length === 0) {
    return <div style={{ color: "#555", padding: 20 }}>No events yet. Run a diagnosis.</div>;
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
      {events.map((e) => (
        <EventRow key={e.id} event={e} selected={selectedId === e.id} onSelect={onSelect} />
      ))}
    </div>
  );
}

function EventRow({ event: e, selected, onSelect }: { event: Event; selected: boolean; onSelect: (id: number) => void }) {
  const color = STATUS_COLORS[e.status] || "#666";
  const icon = STATUS_ICONS[e.status] || "?";
  const stackTag = e.pipe_stack === "cache" ? "[c]" : e.pipe_stack === "consolidate" ? "[s]" : "   ";

  return (
    <button
      onClick={() => onSelect(e.id)}
      style={{
        display: "block",
        width: "100%",
        textAlign: "left",
        padding: "8px 12px",
        background: selected ? "#1a1a2e" : "transparent",
        border: selected ? `1px solid ${color}44` : "1px solid transparent",
        borderRadius: 4,
        cursor: "pointer",
        fontFamily: "monospace",
        color: "#e0e0e0",
      }}
    >
      <div style={{ display: "flex", gap: 8, alignItems: "baseline", fontSize: "0.8rem" }}>
        <span style={{ color: "#555" }}>{e.source_date}</span>
        <span style={{ color: "#555" }}>{stackTag}</span>
        <span style={{ color: "#888" }}>{e.pipe_site}</span>
        <span style={{ color, fontWeight: "bold" }}>{icon} {e.status}</span>
      </div>
      <div
        style={{
          fontSize: "0.75rem",
          color: "#888",
          marginTop: 2,
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
        }}
      >
        {e.evidence}
      </div>
      {e.source_url && (
        <a
          href={e.source_url}
          target="_blank"
          rel="noopener"
          onClick={(ev) => ev.stopPropagation()}
          style={{ fontSize: "0.65rem", color: "#444", textDecoration: "none" }}
        >
          {new URL(e.source_url).hostname} ↗
        </a>
      )}
    </button>
  );
}
