import { CATEGORY_COLORS } from "../types";

interface Props {
  category: string | null;
  outcome: string | null;
  runwayMonths: number | null;
}

export function HealthLED({ category, outcome, runwayMonths }: Props) {
  const color = category ? CATEGORY_COLORS[category] || "#666" : "#333";
  const isPending = outcome === "pending";
  const isCritical = runwayMonths !== null && runwayMonths < 6;

  return (
    <div style={{ position: "fixed", top: 16, right: 20, textAlign: "right", zIndex: 100 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, justifyContent: "flex-end" }}>
        <div
          className={isPending || isCritical ? "pulse" : ""}
          style={{
            width: 28,
            height: 28,
            borderRadius: "50%",
            background: `radial-gradient(circle at 35% 35%, rgba(255,255,255,0.4), transparent 60%), radial-gradient(circle, ${color}, ${color}88)`,
            boxShadow: `0 0 8px ${color}, inset 0 1px 2px rgba(255,255,255,0.3)`,
            border: "2px solid #333",
          }}
        />
        {runwayMonths !== null && (
          <span
            className={isCritical ? "pulse" : ""}
            style={{ color, fontSize: "1.1rem", fontWeight: "bold", fontFamily: "monospace" }}
          >
            {runwayMonths}mo
          </span>
        )}
      </div>
      {category && (
        <div style={{ fontSize: "0.65rem", color: "#555", marginTop: 4, fontFamily: "monospace" }}>
          {category.replace("_", " ")}
        </div>
      )}
    </div>
  );
}
