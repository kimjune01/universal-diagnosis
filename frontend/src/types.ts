export interface CompanySummary {
  id: number;
  ticker: string;
  name: string;
  category: string | null;
  direction: string | null;
  outcome: string | null;
  event_count: number;
}

export interface Pipe {
  id: number;
  description: string;
  stack: "cache" | "consolidate" | null;
  site: string | null;
  depth: number;
}

export interface Event {
  id: number;
  pipe_id: number;
  pipe_site: string;
  pipe_stack: string;
  source_date: string;
  status: "functional" | "broken" | "stressed" | "repaired" | "unknown";
  evidence: string;
  source_url: string;
}

export interface Prediction {
  id: number;
  category: string;
  direction: string;
  catalyst: string;
  resolution_source: string;
  window_start: string;
  window_end: string;
  pass_condition: string;
  reasoning: string;
  run: string;
  outcome: string;
}

export interface Analyst {
  analyst_name: string;
  direction: string;
  source_url: string;
  call_date: string;
}

export interface Financials {
  cash: number;
  quarterly_burn: number;
  source_date: string;
  source_url: string | null;
  runway_quarters: number | null;
  runway_months: number | null;
}

export interface CompanyDetail {
  ticker: string;
  name: string;
  pipes: Pipe[];
  events: Event[];
  prediction: Prediction | null;
  analyst: Analyst | null;
  financials: Financials | null;
}

export interface Stats {
  n: number;
  resolved: number;
  hits: number;
  misses: number;
  pending: number;
  accuracy: number | null;
  p_value: number | null;
  base_rate: number;
}

export const STATUS_COLORS: Record<string, string> = {
  functional: "#4ade80",
  broken: "#f87171",
  stressed: "#fbbf24",
  repaired: "#60a5fa",
  unknown: "#666",
};

export const STATUS_ICONS: Record<string, string> = {
  functional: "✓",
  broken: "✗",
  stressed: "~",
  repaired: "↑",
  unknown: "?",
};

export const CATEGORY_COLORS: Record<string, string> = {
  living_well: "#4ade80",
  dying_pivoted: "#fbbf24",
  living_dying: "#fb923c",
  dying_dying: "#f87171",
};

export const OUTCOME_ICONS: Record<string, string> = {
  hit: "✓",
  miss: "✗",
  pending: "◌",
  void: "—",
};
