# Pre-registration: Ongoing Scorecard

**Status**: Active. N grows as Shkreli takes public positions.

## Research question

Does a seven-pipe, one-level temporal graph of a biotech company's learning loop, built from dated public records, predict binary catalyst outcomes better than (a) a domain expert's snapshot analysis, and (b) the same framework without temporal ordering?

## Design

Follow Shkreli's public biotech positions as they appear. Each company gets **three locked predictions** before the catalyst:

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
Every biotech company where Shkreli takes a public, timestamped, directional position (long/short/bull/bear) gets diagnosed. No cherry-picking. If he tweets it, we run it.

### Inclusion criteria
- Shkreli has a public, timestamped, directional position (X post, interview, report)
- Company has a binary catalyst within 12 months (trial readout, FDA action, regulatory filing)
- At least 3 dated public records exist before the catalyst (enough for a temporal graph)
- Listed options available at time of catalyst (Hypothesis 2 only)

### Exclusion criteria
- Non-biotech positions (computing, crypto, etc.)
- Positions without a clear directional call (vague commentary, "interesting company")
- Companies with fewer than 3 dated public records

### Stopping rule
If Shkreli stops covering a stock (goes silent, position closed, company acquired or delisted), the prediction resolves on whatever ground truth exists at that point or is voided if no catalyst occurred within the window. We don't keep diagnosing companies he's moved on from.

### Expected sample size
Shkreli takes 5-10 public biotech positions per year. At that rate, N=10 within 1-2 years. N=30 within 3-5 years.

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
2. **Look-ahead bias**: temporal graph must be built strictly from records dated before the catalyst. Enforceable because every event has a source_date.
3. **Classification bias**: the framework author (us) also runs the diagnosis. Mitigated by mechanical scoring and audit trail.
4. **Small N**: significance accumulates slowly. The dashboard shows convergence but may never reach p < 0.05. That's a result, not a failure.

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
