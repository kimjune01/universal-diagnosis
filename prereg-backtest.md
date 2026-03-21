# Pre-registration: Backtest + Ongoing Scorecard

**Status**: Active. Two phases: historical backtest (2020-2025), then ongoing as Shkreli takes new positions.

## Research question

Does a seven-pipe, one-level temporal graph of a biotech company's learning loop, built from dated public records, predict binary catalyst outcomes better than (a) a domain expert's snapshot analysis, and (b) the same framework without temporal ordering?

## Design

Two phases, same method, same scoring.

### Phase 1: Historical backtest (2020-2025)

Pull every public biotech position Shkreli took from his release (May 2022) through December 2025. Build temporal graphs from records dated *before* each catalyst. Predict and score against known outcomes. This gives us N=20-30 immediately and tests the hypothesis before any new positions are needed.

**Critical constraint**: the temporal graph for each company must be built strictly from records with archival dates before the catalyst. No look-ahead. The outcome is known to us but the graph must not contain it.

### Phase 2: Ongoing scorecard (2026+)

Follow Shkreli's new positions as they appear. Same method as Phase 1 but prospective — predict before the catalyst, score after.

### Both phases

Each company gets **three locked predictions** before the catalyst (or before scoring, for Phase 1):

1. **Temporal-graph prediction** — full framework with event ordering, trajectory category, transition analysis
2. **Snapshot-only prediction** — same seven pipes, same evidence, but only latest status per pipe (no trajectory, no recurrence check, no transition history). Category derived from current state, not trajectory.
3. **Analyst prediction** — Shkreli's public call mapped to PASS/FAIL on the same catalyst

The temporal vs. snapshot comparison isolates whether temporal ordering adds signal. The temporal vs. analyst comparison tests whether the framework beats domain expertise.

### Hypothesis 1: Temporal graph beats snapshot

The temporal-graph prediction outperforms the snapshot-only prediction on binary catalyst accuracy.

### Hypothesis 2: Temporal graph beats analyst

The temporal-graph prediction outperforms Shkreli's call on the same catalysts.

### Hypothesis 3: Vol mispricing

Companies diagnosed with broken read_outcomes exhibit higher realized-to-implied vol ratios around catalyst dates than companies with functional read_outcomes.

## Sample

### Selection rule
Every biotech company where Shkreli took or takes a public, timestamped, directional position (long/short/bull/bear) gets diagnosed. No cherry-picking. If he tweeted it, we run it.

### Phase 1 discovery
Search Shkreli's public record (X/Twitter, YouTube, interviews, financial media coverage) from May 2022 (prison release) through December 2025 for every biotech position with a resolvable catalyst. Archive each source URL and screenshot. This discovery is done once, before any diagnosis begins. The full list is frozen before processing any company.

### Inclusion criteria
- Shkreli has a public, timestamped, directional position (X post, interview, report)
- Company has a binary catalyst within 12 months of the position (trial readout, FDA action, regulatory filing)
- At least 3 dated public records exist before the catalyst (enough for a temporal graph)
- Catalyst has resolved (Phase 1) or will resolve within 12 months (Phase 2)
- Listed options available at time of catalyst (Hypothesis 3 only)

### Exclusion criteria
- Non-biotech positions (computing, crypto, etc.)
- Positions without a clear directional call (vague commentary, "interesting company")
- Companies with fewer than 3 dated public records
- Catalysts that are ambiguous or unresolvable (no clear binary outcome)

### Eviction policy (Phase 2 only)

Companies are evicted from active tracking under four conditions:

- **Resolved**: catalyst occurred, outcome scored (hit/miss). Company moves to historical record.
- **Voided**: catalyst window expired with no binary event. Scored as void, evicted from active tracking.
- **Stale**: no public Shkreli statement about the company in 6 months. Evicted. Any pending prediction resolves on whatever ground truth exists at eviction date, or is voided if no catalyst occurred.
- **Dead**: company acquired, delisted, or entered bankruptcy. Pending prediction voided, evicted.

The 6-month staleness rule prevents tracking zombie positions where Shkreli quietly exited. If he's still talking about it, we keep tracking. If he's moved on, so do we.

### Expected sample size
- **Phase 1**: Shkreli has been publicly active on biotech since mid-2022. Estimated 20-30 resolvable positions. All outcomes known.
- **Phase 2**: 5-10 new positions per year. N grows organically.
- **Combined**: N=25-40 at launch of Phase 2, growing from there.

## Data sources

All public, all free or cheap:
- **ClinicalTrials.gov API**: trial designs, endpoints, results, amendments, posting dates
- **SEC EDGAR**: 10-K, 10-Q, 8-K filings with filing dates
- **PubMed**: published trial results with publication dates
- **FDA databases**: approval letters, CRLs, meeting minutes with issuance dates
- **CRSP / Yahoo Finance**: daily stock prices around catalyst dates
- **CBOE / OptionMetrics**: 30-day implied volatility before catalyst (Hypothesis 2; may require paid data)
- **Shkreli's public posts**: X (Twitter), YouTube, Substack, interviews — with timestamps and URLs

## Method

### For each new Shkreli position:

1. **Record the analyst call**: Shkreli's post URL, date, direction (bull/bear), and the specific catalyst he's calling. This is the audit trail entry point.

2. **Define the catalyst**: exact event, resolution source, window, pass condition. Same template as the pilot. Lock before any diagnosis.

3. **Build temporal graph** from public records dated before the catalyst. Each record is an event with: pipe, source_date, status, evidence, source_url. Same schema as the pilot.

4. **Classify trajectory** using the same agent protocol: 4 search agents, top-2 selection, 2 merge instances, soap-a default on disagreement. Category assigned: living_well, living_dying, dying_pivoted, dying_dying.

5. **Map category to direction**: living_well/dying_pivoted → PASS, living_dying/dying_dying → FAIL.

6. **Generate snapshot-only prediction**: same seven pipes, same events, but ignore temporal ordering. Use only the latest status per pipe. Classify category from current state (all functional = living_well, any broken with no repairs = dying_dying, etc.). Record PASS/FAIL independently from the temporal prediction.

7. **Compute graph features**: recurrence count, transition count, repair latency, pipe coverage, etc. Store alongside both predictions.

8. **Record confidence**: high/medium/low for temporal prediction (based on merge agreement and trajectory clarity). Infer analyst confidence from Shkreli's language.

9. **Publish both predictions** (temporal and snapshot-only) before catalyst date. Commit to repo with timestamp.

10. **Score against ground truth**: check resolution source on window_end. Binary: pass condition met or not. Score all three arms (temporal, snapshot, analyst) against the same ground truth.

11. **For Hypothesis 3**: Pull 30-day implied vol before catalyst date, compute 5-day realized vol around catalyst. Compute ratio. Tag company with read_outcomes status.

## Graph-derived features (collected at prediction time)

For each company at the moment of prediction, compute and store:
- **Recurrence count**: number of pipes where the same failure class appeared more than once
- **Transition count**: total status changes across all pipes
- **Repair latency**: days from most recent break event to most recent repair event (per pipe)
- **Days since last event**: staleness of the temporal graph
- **Pipe coverage**: fraction of seven pipes with at least one event (0-1)
- **Failure-to-repair path**: boolean — does at least one pipe show a broken → repaired trajectory?
- **Event density**: total events / months of coverage

These features are computable from the events we already collect. Store them alongside the prediction record so that post-hoc analysis can identify which features drive accuracy.

## Confidence

Each prediction records a confidence level:
- **Framework confidence**: high / medium / low (or 0-1 scale)
  - High: both merges agree, strong trajectory signal, no ambiguous pipes
  - Medium: merges disagree (soap-a default used), or trajectory is mixed
  - Low: sparse events, multiple unknown pipes, trajectory unclear
- **Analyst confidence**: inferred from Shkreli's language
  - High: explicit position with price target or strong language ("will not work", "will be approved")
  - Medium: directional lean without conviction language
  - Low: hedged or conditional statement

Confidence is not part of binary scoring but enables calibration analysis if N grows large enough.

## Audit trail

Every prediction must have a complete chain of provenance:

1. **Shkreli source**: URL + screenshot/archive of his public position with timestamp
2. **Search reports**: 4 agent outputs saved to `searches/{TICKER}/`
3. **SOAP notes**: 2 merge outputs saved to `notes/{TICKER}/`
4. **Diagnosis**: final prediction record saved to `diagnoses/{TICKER}.md`
5. **DB record**: all fields populated in `prediction` table with `published_at` set
6. **Ground truth**: URL to the press release or 8-K that resolves the catalyst

Every event in the temporal graph has a `source_url` pointing to the public record. If the URL dies, the archival date and evidence text remain. The chain runs: Shkreli post → agent search → events with URLs → SOAP merge → prediction → ground truth.

## Scoring

### Hypothesis 1: Temporal beats snapshot
- **Primary metric**: temporal accuracy vs. snapshot-only accuracy on the same catalysts
- **Statistical test**: McNemar's test (paired binary outcomes on same companies)
- **This is the core test** — it isolates whether temporal ordering adds signal

### Hypothesis 2: Temporal beats analyst
- **Primary metric**: temporal accuracy vs. Shkreli accuracy on the same catalysts
- **Secondary**: both vs. naive base rate (50%)
- **Statistical test**: McNemar's test (paired)
- **Realistic expectation**: N will grow slowly. Significance may take years. Dashboard shows convergence.

### Hypothesis 3: Vol mispricing
- **Primary metric**: mean realized/implied vol ratio, segmented by read_outcomes status
- **Minimum group size**: 5 per group before computing (small N acknowledged)
- **This hypothesis is tertiary** — runs in parallel, may never reach statistical power

## Known biases

1. **Selection bias**: we only diagnose companies Shkreli covers. His picks skew toward controversial, high-volatility names. Not a random sample of biotech.
2. **Look-ahead bias (Phase 1)**: we know the outcomes. The temporal graph must be built strictly from records with archival dates before the catalyst. Enforceable because every event has a source_date. But the diagnostician (us) knows the answer, which may unconsciously influence status labeling. Mitigated by: (a) mechanical scoring, (b) snapshot-only arm as control (same diagnostician bias applies to both, so the temporal-vs-snapshot comparison is fair even if both are biased).
3. **Classification bias**: the framework author (us) also runs the diagnosis. Mitigated by mechanical scoring, audit trail, and the snapshot-only arm.
4. **Hindsight in Phase 1**: Shkreli's historical positions are already scored by the market. We might unconsciously select positions where the framework would look good. Mitigated by: freeze the full list of positions before diagnosing any company. Process all of them, not a subset.
5. **Small N**: Phase 1 gives N=20-30, which is borderline for McNemar's test. The dashboard shows convergence. Phase 2 adds power over time.
6. **LLM knowledge contamination (Phase 1)**: the LLM agents may have been trained on data that includes the outcomes of 2020-2025 catalysts. The agents are instructed to report events with archival dates and evidence from public records, not to predict outcomes. But latent knowledge of outcomes could influence status labeling. This bias affects all three arms equally if using the same LLM, so the temporal-vs-snapshot comparison remains valid.

## Success criterion

**Descriptive**: all three arms (temporal, snapshot, analyst) reported side by side after each resolution. No inferential claim until N >= 20.

**Inferential** (if N reaches 20+):
- H1: temporal accuracy > snapshot accuracy at p < 0.05 (McNemar's)
- H2: temporal accuracy > analyst accuracy at p < 0.05 (McNemar's)
- Either can succeed or fail independently.

**Vol hypothesis**: reported descriptively at any N. Inferential only if both groups reach N >= 10.

## Commitment

- Diagnose every Shkreli biotech position we become aware of (no cherry-picking)
- Publish prediction before catalyst date
- Publish outcome regardless of result
- Maintain complete audit trail (Shkreli source URL → search reports → SOAP notes → diagnosis → ground truth URL)
- Update dashboard and scorecard.json after each resolution
- Report misses at same prominence as hits

## Cost estimate

Per company: ~$0.50-1.50 in LLM API calls (4 agents + 2 merges). At 5-10 companies/year: **$5-15/year**. The dashboard is free (static HTML + JSON).
