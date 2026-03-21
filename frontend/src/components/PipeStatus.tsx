import { Pipe, Event, STATUS_COLORS, STATUS_ICONS } from "../types";

interface Props {
  pipes: Pipe[];
  events: Event[];
  selectedEventId: number | null;
}

export function PipeStatus({ pipes, events, selectedEventId }: Props) {
  const cachePipes = pipes.filter((p) => p.stack === "cache");
  const consolidatePipes = pipes.filter((p) => p.stack === "consolidate");

  const getStatus = (pipeId: number) => {
    const relevant = events
      .filter((e) => e.pipe_id === pipeId && (selectedEventId === null || e.id <= selectedEventId))
      .sort((a, b) => b.id - a.id);
    return relevant[0]?.status || null;
  };

  return (
    <div style={{ fontSize: "0.8rem", fontFamily: "monospace" }}>
      <PipeGroup label="CACHE STACK" pipes={cachePipes} getStatus={getStatus} />
      <div style={{ height: 12 }} />
      <PipeGroup label="CONSOLIDATE STACK" pipes={consolidatePipes} getStatus={getStatus} />
    </div>
  );
}

function PipeGroup({
  label,
  pipes,
  getStatus,
}: {
  label: string;
  pipes: Pipe[];
  getStatus: (id: number) => string | null;
}) {
  return (
    <div>
      <div style={{ color: "#555", fontSize: "0.65rem", letterSpacing: "0.1em", marginBottom: 4 }}>{label}</div>
      {pipes.map((p) => {
        const status = getStatus(p.id);
        const color = status ? STATUS_COLORS[status] : "#333";
        const icon = status ? STATUS_ICONS[status] : "—";
        const statusLabel = status || "—";

        return (
          <div key={p.id} style={{ display: "flex", justifyContent: "space-between", padding: "3px 0" }}>
            <span style={{ color: "#888" }}>{p.site}</span>
            <span style={{ color, fontWeight: status ? "bold" : "normal" }}>
              {icon} {statusLabel}
            </span>
          </div>
        );
      })}
    </div>
  );
}
