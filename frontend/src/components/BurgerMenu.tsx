import { CompanySummary, OUTCOME_ICONS } from "../types";

interface Props {
  companies: CompanySummary[];
  selected: string;
  open: boolean;
  onToggle: () => void;
  onSelect: (ticker: string) => void;
  onScorecard: () => void;
}

export function BurgerMenu({ companies, selected, open, onToggle, onSelect, onScorecard }: Props) {
  const run0 = companies.filter((c) => {
    // CAPR and QURE are run0
    return c.ticker === "CAPR" || c.ticker === "QURE";
  });
  const run1 = companies.filter((c) => c.ticker !== "CAPR" && c.ticker !== "QURE");

  return (
    <>
      <button
        onClick={onToggle}
        style={{
          position: "fixed",
          top: 14,
          left: 16,
          zIndex: 200,
          background: "none",
          border: "none",
          color: "#e0e0e0",
          fontSize: "1.4rem",
          cursor: "pointer",
          padding: 4,
        }}
      >
        ☰
      </button>

      {open && (
        <div
          onClick={onToggle}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.5)",
            zIndex: 150,
          }}
        />
      )}

      <div
        style={{
          position: "fixed",
          top: 0,
          left: open ? 0 : -200,
          width: 180,
          height: "100vh",
          background: "#111",
          borderRight: "1px solid #222",
          zIndex: 160,
          transition: "left 0.2s ease",
          padding: "60px 16px 16px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {run0.map((c) => (
          <CompanyItem key={c.ticker} company={c} selected={selected === c.ticker} onSelect={onSelect} />
        ))}

        <div style={{ borderTop: "1px solid #333", margin: "8px 0" }} />

        {run1.map((c) => (
          <CompanyItem key={c.ticker} company={c} selected={selected === c.ticker} onSelect={onSelect} />
        ))}

        <div style={{ flex: 1 }} />

        <button
          onClick={onScorecard}
          style={{
            background: "none",
            border: "1px solid #333",
            color: "#888",
            padding: "6px 12px",
            borderRadius: 4,
            cursor: "pointer",
            fontFamily: "monospace",
            fontSize: "0.8rem",
          }}
        >
          Scorecard
        </button>
      </div>
    </>
  );
}

function CompanyItem({
  company,
  selected,
  onSelect,
}: {
  company: CompanySummary;
  selected: boolean;
  onSelect: (t: string) => void;
}) {
  const icon = company.outcome ? OUTCOME_ICONS[company.outcome] || "?" : "◌";
  const color = company.outcome === "hit" ? "#4ade80" : company.outcome === "miss" ? "#f87171" : "#666";

  return (
    <button
      onClick={() => onSelect(company.ticker)}
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "8px 8px",
        background: selected ? "#1a1a1a" : "transparent",
        border: "none",
        borderRadius: 4,
        color: selected ? "#fff" : "#aaa",
        cursor: "pointer",
        fontFamily: "monospace",
        fontSize: "0.9rem",
        width: "100%",
        textAlign: "left",
      }}
    >
      <span>{company.ticker}</span>
      <span style={{ color }}>{icon}</span>
    </button>
  );
}
