# Bootstrap: Universal Diagnosis

Read this first. Then read `CLAUDE.md`, then `prereg-backtest.md`, then `prereg-stratified.md`.

## What this is

A prediction engine that diagnoses biotech companies using the Natural Framework's temporal pipe graph. Head-to-head with Martin Shkreli. Three live predictions published.

## Status as of March 20, 2026

### Done
- **Phase 1 backtest**: 3/3 correct (CAPR, QURE, SAVA). Framework beat Shkreli on CAPR.
- **Phase 2 live predictions**: SPRB PASS (by Dec 31), ATYR PASS (by Sep 30), INMB FAIL (by Sep 30)
- **Blog post**: june.kim/diagnosis-biotech
- **Dashboard MVP**: FastAPI + React viewer at localhost:8000/5173
- **Three preregs**: Shkreli scorecard (active), market comparison (deferred), stratified backtest (ready to execute)

### Next session priorities
1. **Run the stratified backtest**: pull ClinicalTrials.gov Phase 3 population, compute hype scores, sample 2×2, process N=100
2. **Load events into DB**: parse EVENT records from search report markdowns into the `event` table
3. **Snapshot-only arm**: run QURE and SAVA through snapshot classification table (owed from Phase 1)
4. **Monitor Phase 2**: ATYR FDA Type C meeting mid-April is the first leading indicator

### Key files
- `prereg-backtest.md` — Shkreli scorecard (active, Phase 1 done, Phase 2 live)
- `prereg-stratified.md` — stratified backtest (ready to execute, N=100)
- `prereg-market.md` — market comparison (deferred, 6 blockers)
- `phase1-results.md` — Phase 1 results (3/3)
- `results.md` — public scorecard
- `worklog/WORK_LOG.md` — full session history
- `schema.sql` — temporal pipe graph schema (3-arm predictions, events, financial snapshots)
- `prompts/` — agent prompts for search and merge
- `diagnoses/` — prediction records (SPRB, ATYR, INMB, SAVA)
- `searches/` — raw agent outputs per company
- `notes/` — SOAP merge outputs per company
- `smoke-test/CAPR/` — static-framing baseline (retroactive snapshot arm)
- `speculation.md` — trade thought experiments (not advice)
- `dashboard-v2-spec.md` — viewer spec

### How to run a diagnosis
```bash
# Start servers
uv run python server.py &
cd frontend && pnpm dev &

# Init DB
uv run python init_db.py

# View a company
uv run python diagnose.py timeline CAPR
uv run python diagnose.py transitions CAPR
uv run python diagnose.py scorecard
```

### How to diagnose a new company
1. Dispatch 4 search agents (2 cache, 2 consolidate) per `prompts/`
2. Save to `searches/{TICKER}/`
3. Select top 2, merge with codex into SOAP notes per `prompts/merge-agent.md`
4. Save to `notes/{TICKER}/`
5. Record prediction in `diagnoses/{TICKER}.md` and DB
6. soap-a is primary on disagreement

### The hypothesis
A seven-pipe, one-level temporal graph of a biotech company's learning loop, built from dated public records, predicts binary catalyst outcomes better than a domain expert's snapshot analysis.

### The four buckets
- **living_well**: both stacks functional → PASS
- **living_dying**: cache functional, consolidate broken → FAIL (but cash buys time)
- **dying_pivoted**: was broken, trajectory shows repair → PASS
- **dying_dying**: both stacks broken, no repair → FAIL
