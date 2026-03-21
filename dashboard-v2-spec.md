# Dashboard v2: CRUD Diagnosis Viewer

## Overview

CRUD app for managing and viewing biotech diagnoses. FastAPI backend serving the existing SQLite database. React + Vite frontend. One company at a time. Discrete event stepping, not a continuous scrubber.

## Architecture

```
FastAPI (Python) ─── SQLite (existing schema)
     │
     └── REST API ─── React + Vite (TypeScript)
```

No JSON export file. The frontend queries the API, which queries the DB directly. Same diagnosis.db the CLI tools already use.

## API endpoints

### Companies
- `GET /companies` — list all companies with latest bucket and prediction status
- `GET /companies/{ticker}` — company detail: pipes, events, financials, prediction

### Events
- `GET /companies/{ticker}/events` — all events for a company, chronological
- `GET /companies/{ticker}/events?before={date}` — events before a date (for time travel)
- `POST /companies/{ticker}/events` — add an event (from agent output or manual entry)

### Pipes
- `GET /companies/{ticker}/pipes` — pipe topology (stable, doesn't change)
- `GET /companies/{ticker}/pipes/status?at={date}` — latest status per pipe as of a date (most recent event per pipe before that date)

### Predictions
- `GET /predictions` — all predictions with outcomes (the scorecard)
- `POST /predictions` — record a new prediction
- `PATCH /predictions/{id}` — score a prediction (set outcome)

### Analyst calls
- `POST /predictions/{id}/analyst` — record Shkreli's position
- `GET /predictions/{id}/analyst` — get Shkreli's position

### Stats
- `GET /stats` — running accuracy, p-value, N, hits, misses, pending

## Frontend: single company view

### Company selector (top bar)
Dropdown or tab bar of tickers. Click one to load its view. Badge showing prediction direction and outcome status.

### Event timeline (main panel)
Vertical list of events, chronological, newest at top. Each event shows:
- Date (source_date)
- Pipe name + stack indicator (cache/consolidate)
- Status chip (colored: green/red/yellow/blue/gray)
- Evidence text (truncated, click to expand)
- Source URL (link icon)

Click an event to "time travel" — everything below updates to show state as of that event's date.

### Pipe status panel (sidebar)
Flat grouped list (not animated tree). Two groups: cache stack, consolidate stack. Each pipe shows its status as of the selected date.

```
CACHE STACK (forward pass)
  perceive_cache      ✓ functional
  cache_filter        ~ stressed
  filter_attend       ↑ repaired
  attend_remember     ? unknown

CONSOLIDATE STACK (backward pass)
  read_outcomes       ✗ broken
  batch_process       ✓ functional
  write_substrate     ✓ functional
```

Status chips update when you click a different event (time travel).

### Bucket + Runway card (sidebar, below pipes)
One card showing:
- Current bucket: living_well / living_dying / dying_pivoted / dying_dying
- Cash: $XXM
- Quarterly burn: $XXM/q
- Runway: N quarters (progress bar, green > 8q, yellow 4-8q, red < 4q)
- As-of date for the financial data

### Prediction card (sidebar, bottom)
- Direction: PASS / FAIL
- Catalyst description
- Window: start → end (days remaining)
- Shkreli: bull / bear (with source link)
- Merges agree: yes / no
- Outcome: pending / hit / miss

## Frontend: scorecard view

Separate route `/scorecard`. The existing dashboard.html table, but now powered by the API instead of polling a JSON file. Shows:
- All predictions in a table
- Running accuracy and p-value
- Convergence bar (at N >= 10)

## Data additions needed

The existing schema has companies, pipes, events, predictions, analyst_calls. What's missing:

### Financial snapshots
```sql
CREATE TABLE IF NOT EXISTS financial_snapshot (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    cash INTEGER NOT NULL,              -- in dollars
    quarterly_burn INTEGER NOT NULL,    -- in dollars
    source_date TEXT NOT NULL,          -- when this was reported
    source_url TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

Multiple snapshots per company — runway changes over time. The API computes current runway as `cash / quarterly_burn` from the most recent snapshot.

### Bucket derivation
Bucket is derived, not stored. The API computes it from the latest pipe statuses:
- All pipes functional or repaired → `living_well`
- Cache stack functional, consolidate has broken pipes → `living_dying`
- Has broken → repaired transitions in recent events → `dying_pivoted`
- Multiple broken pipes, no repairs → `dying_dying`

Or: just use the prediction's `category` field, which was set during diagnosis.

## Tech stack

- **Backend**: FastAPI, uvicorn, sqlite3 (stdlib, no ORM)
- **Frontend**: Vite + React + TypeScript, pnpm
- **Styling**: Tailwind or plain CSS, dark theme (match existing dashboard.html aesthetic)
- **No auth** — local tool, not deployed

## MVP scope

1. API serving existing data (companies, pipes, events, predictions)
2. Company selector + event timeline + pipe status panel
3. Click event to time travel (pipe statuses update)
4. Prediction card with Shkreli comparison
5. Scorecard view with running accuracy

## Not MVP

- Financial snapshot CRUD (hardcode from known data initially)
- Bucket derivation from pipe states (use prediction.category)
- Cross-company comparison view
- Animated anything
- Mobile responsive
- Deployment
