# Dashboard v2: Diagnosis Viewer

## Overview

Read-only event explorer for biotech diagnoses. FastAPI backend serving the existing SQLite database. React + Vite frontend. One company at a time. Time travel by clicking events.

**Scale**: tens of companies, hundreds of events. Local tool, not deployed.

## Architecture

```
FastAPI (Python) ─── SQLite (diagnosis.db)
     │
     └── REST API ─── React + Vite (TypeScript)
```

No JSON export. The frontend queries the API. Same DB the CLI tools use.

## API

### `GET /companies`

Returns all companies with their prediction summary. Denormalized — one query, no N+1.

```json
[
  {
    "ticker": "CAPR",
    "name": "Capricor Therapeutics",
    "category": "dying_pivoted",
    "direction": "pass",
    "outcome": "hit",
    "event_count": 38
  }
]
```

### `GET /companies/{ticker}`

One aggregate endpoint for the full company view. Returns everything the frontend needs in one call.

```json
{
  "ticker": "CAPR",
  "name": "Capricor Therapeutics",
  "pipes": [
    { "id": 2, "description": "Compound enters biological system", "stack": "cache", "site": "perceive_cache", "depth": 1 }
  ],
  "events": [
    { "id": 1, "pipe_id": 2, "pipe_site": "perceive_cache", "source_date": "2012-02-14", "status": "functional", "evidence": "CADUCEUS: intracoronary CDCs reach myocardium", "source_url": "https://pubmed.ncbi.nlm.nih.gov/22336189/" }
  ],
  "prediction": {
    "id": 1,
    "category": "dying_pivoted",
    "direction": "pass",
    "catalyst": "HOPE-3 Phase 3 topline",
    "resolution_source": "Capricor press release or SEC 8-K",
    "window_start": "2025-10-01",
    "window_end": "2025-12-31",
    "pass_condition": "PUL v2.0 total score statistically significant",
    "reasoning": "Consolidate stack functional across four iterations",
    "outcome": "hit"
  },
  "analyst": {
    "analyst_name": "Martin Shkreli",
    "direction": "fail",
    "source_url": "https://x.com/MartinShkreli/status/...",
    "call_date": "2025-11-24"
  },
  "financials": {
    "cash": 318000000,
    "quarterly_burn": 26000000,
    "source_date": "2025-12-31",
    "runway_quarters": 12
  }
}
```

Events returned ascending by source_date. All dates are ISO 8601 date-only (YYYY-MM-DD).

### `GET /predictions`

The scorecard. All published predictions with analyst calls and outcomes.

### `GET /stats`

Running accuracy, p-value vs 50% base rate, N, hits, misses, pending.

## Frontend

### State model

```
selectedTicker: string
selectedEventId: number | null     // null = latest (current state)
companyData: CompanyResponse       // from GET /companies/{ticker}
```

Everything derives from these three values:
- **Pipe statuses**: for each pipe, find the most recent event with `event.id <= selectedEventId`. That event's status is the pipe's status at the selected point in time.
- **Bucket**: `companyData.prediction.category` (not derived from pipe states in MVP)
- **Runway**: `companyData.financials.runway_quarters` (static in MVP, not time-traveled)

### Company nav (burger menu → slide-out panel)

Hamburger icon top-left. Click to slide out a narrow panel with vertical ticker list. Each entry shows ticker + colored outcome chip. Selected company highlighted. Click a ticker to load its data and close the panel. Run 0 and Run 1 separated by a divider.

```
  ☰
  ┌──────────┐
  │ CAPR  ✓  │
  │ QURE  ✓  │
  │ ──────── │
  │ SPRB  ◌  │
  │ ATYR  ◌  │
  │ INMB  ◌  │
  │          │
  │ Scorecard│
  └──────────┘
```

Panel also has a "Scorecard" link at the bottom to switch to the scorecard view. Clicking outside the panel or pressing Esc closes it.

### Event timeline (main panel)

Vertical list, ascending (oldest at top, newest at bottom — reading order matches temporal flow).

Each event row:
```
2020-09-21  [c] filter_attend   ✗ broken
ALLSTAR publication: primary endpoint failed (scar size wrong readout)
                                                    pubmed.ncbi.nlm.nih.gov ↗
```

- Date, stack tag `[c]`/`[s]`, pipe site, status chip
- Evidence text (one line, truncated, click to expand)
- Source URL as a subtle link
- Selected event has a highlighted border
- Click any event → selectedEventId updates → pipe status panel recomputes

### Pipe status panel (sidebar)

Two groups. Each pipe shows status as of selectedEventId.

```
CACHE STACK
  perceive_cache      ✓ functional
  cache_filter        ~ stressed
  filter_attend       ↑ repaired
  attend_remember     ? unknown

CONSOLIDATE STACK
  read_outcomes       ✗ broken
  batch_process       ✓ functional
  write_substrate     ✓ functional
```

If no event exists for a pipe at the selected time, show `—` (no data yet).

Status colors: green=functional, red=broken, yellow=stressed, blue=repaired, gray=unknown.

### Prediction card (sidebar, below pipes)

```
PREDICTION: PASS (dying_pivoted)
Catalyst: HOPE-3 Phase 3 topline
Window: 2025-10-01 → 2025-12-31
Pass condition: PUL v2.0 significant
Outcome: HIT ✓

ANALYST: Martin Shkreli — FAIL
Source: x.com/MartinShkreli/... ↗
Date: 2025-11-24
```

### Runway card (sidebar, bottom)

```
RUNWAY
Cash: $318M  Burn: $26M/q  Runway: 12q
████████████████████░░░░ as of 2025-12-31
```

Progress bar: green > 8q, yellow 4-8q, red < 4q.

### Scorecard view (`/scorecard`)

Table of all predictions. Running accuracy and p-value. Same data as v1 dashboard but from the API.

## Data addition

One new table for financials:

```sql
CREATE TABLE IF NOT EXISTS financial_snapshot (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    cash INTEGER NOT NULL,
    quarterly_burn INTEGER NOT NULL,
    source_date TEXT NOT NULL,
    source_url TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

API returns latest snapshot per company. Runway = `cash / quarterly_burn` computed server-side.

## Tech stack

- **Backend**: FastAPI, uvicorn, sqlite3 (no ORM)
- **Frontend**: Vite + React + TypeScript, pnpm
- **Styling**: plain CSS, dark background (#0a0a0a), monospace font, minimal — same feel as v1

## Empty states

- No events for a company: "No events yet. Run a diagnosis."
- No prediction: hide prediction card
- No analyst call: hide analyst section of prediction card
- No financial snapshot: hide runway card
- Pipe with no events at selected time: show `—`
