# Universal Diagnosis

Generate falsifiable predictions from the Natural Framework. Biotech pilot: head-to-head with Martin Shkreli's public calls.

## Goal

Legitimize the Natural Framework by publishing timestamped predictions that outperform domain expert analysts. The molecule is the pipe, the company is its consolidate stack.

## Key files

- `design.md` — full design: goal, prediction types, runs, coordination protocol
- `biotech.md` — biotech pilot: org-chart mapping, analyst head-to-head, data sources
- `prereg.md` — pre-registration for scientific accountability
- `taxonomy.md` — recursive pipe tree (self-similar, no privileged scales)
- `probes.md` — diagnostic probes by stack and fault site
- `worklog.md` — running log of decisions and progress

## Scripts

- `init_db.py` — create DB, seed companies and traumas
- `embed.py` — embed descriptions for semantic matching (all-MiniLM-L6-v2)
- `diagnose.py` — CLI: `timeline TICKER`, `transitions TICKER`, `scorecard`
- `schema.sql` — SQLite schema (temporal: pipes, events, predictions)
- `prompts/` — agent prompts (cache, consolidate, merge)

## Commands

```bash
uv run python init_db.py                      # initialize/reset database
uv run python embed.py                        # embed unembedded pipes and traumas
uv run python diagnose.py timeline CAPR       # show event timeline per pipe
uv run python diagnose.py transitions CAPR    # show status changes only
uv run python diagnose.py scorecard           # show prediction scorecard
```

## Related

- Blog: `the-parts-bin.md` — algorithm catalog, Attend grid
- Blog: `blind-blind-merge.md` — the expensive solution this replaces
- Blog: `diagnosis-company.md` — applying diagnosis to companies
- Repo: `~/Documents/natural-framework/` — the framework itself
