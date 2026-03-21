import { useEffect, useState } from "react";
import { fetchCompanies, fetchCompany } from "./api";
import { CompanySummary, CompanyDetail } from "./types";
import { BurgerMenu } from "./components/BurgerMenu";
import { HealthLED } from "./components/HealthLED";
import { EventTimeline } from "./components/EventTimeline";
import { PipeStatus } from "./components/PipeStatus";
import { PredictionCard } from "./components/PredictionCard";
import { RunwayCard } from "./components/RunwayCard";

export default function App() {
  const [companies, setCompanies] = useState<CompanySummary[]>([]);
  const [selectedTicker, setSelectedTicker] = useState("CAPR");
  const [companyData, setCompanyData] = useState<CompanyDetail | null>(null);
  const [selectedEventId, setSelectedEventId] = useState<number | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    fetchCompanies().then(setCompanies);
  }, []);

  useEffect(() => {
    setCompanyData(null);
    setSelectedEventId(null);
    fetchCompany(selectedTicker).then((data) => {
      setCompanyData(data);
      // Default to latest event
      if (data.events.length > 0) {
        setSelectedEventId(data.events[data.events.length - 1].id);
      }
    });
  }, [selectedTicker]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMenuOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const handleSelect = (ticker: string) => {
    setSelectedTicker(ticker);
    setMenuOpen(false);
  };

  return (
    <div style={{ background: "#0a0a0a", color: "#e0e0e0", minHeight: "100vh", fontFamily: "'SF Mono', Menlo, monospace" }}>
      <BurgerMenu
        companies={companies}
        selected={selectedTicker}
        open={menuOpen}
        onToggle={() => setMenuOpen(!menuOpen)}
        onSelect={handleSelect}
        onScorecard={() => {/* TODO */}}
      />

      <HealthLED
        category={companyData?.prediction?.category || null}
        outcome={companyData?.prediction?.outcome || null}
        runwayMonths={companyData?.financials?.runway_months || null}
      />

      {/* Header */}
      <div style={{ padding: "16px 16px 8px 52px" }}>
        <h1 style={{ fontSize: "1.3rem", margin: 0 }}>
          {companyData?.ticker || "..."}{" "}
          <span style={{ color: "#555", fontWeight: "normal", fontSize: "0.9rem" }}>
            {companyData?.name || ""}
          </span>
        </h1>
      </div>

      {/* Main layout */}
      <div style={{ display: "flex", gap: 16, padding: "8px 16px 16px 16px" }}>
        {/* Event timeline */}
        <div style={{ flex: 2, maxHeight: "calc(100vh - 80px)", overflowY: "auto" }}>
          {companyData && (
            <EventTimeline
              events={companyData.events}
              selectedId={selectedEventId}
              onSelect={setSelectedEventId}
            />
          )}
        </div>

        {/* Sidebar */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 12, minWidth: 260 }}>
          {companyData && (
            <>
              <PipeStatus
                pipes={companyData.pipes}
                events={companyData.events}
                selectedEventId={selectedEventId}
              />
              <PredictionCard
                prediction={companyData.prediction}
                analyst={companyData.analyst}
              />
              <RunwayCard financials={companyData.financials} />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
