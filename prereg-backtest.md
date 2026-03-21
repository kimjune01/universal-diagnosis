# Pre-registration: Backtest + Ongoing Scorecard

**Status**: Active. Two phases: historical backtest (2022-2025), then ongoing as Shkreli takes new positions.

## Research question

Does a seven-pipe, one-level temporal graph of a biotech company's learning loop, built from dated public records, predict binary catalyst outcomes better than (a) a domain expert's snapshot analysis, and (b) the same framework without temporal ordering?

## Design

Two phases, same method, same scoring.

### Phase 1: Historical backtest (2022-2025)

Pull every qualifying biotech position Shkreli took from his release (May 2022) through December 2025. Build temporal graphs from records dated *before* each catalyst. Predict and score against known outcomes.

**Critical constraint**: the temporal graph for each company must be built strictly from records with archival dates before the catalyst. No look-ahead.

### Phase 2: Ongoing scorecard (2026+)

Follow Shkreli's new positions as they appear. Same method as Phase 1 but prospective.

### Both phases

Each company-catalyst pair gets **three locked predictions**:

1. **Temporal-graph prediction** — full framework with event ordering, trajectory category, transition analysis
2. **Snapshot-only prediction** — same seven pipes, same evidence, but only latest status per pipe (no trajectory, no recurrence check, no transition history). Category derived mechanically from current state per the snapshot classification table below.
3. **Analyst prediction** — Shkreli's public call mapped to PASS/FAIL per the analyst mapping rules below.

### Hypothesis 1: Temporal graph beats snapshot

The temporal-graph prediction outperforms the snapshot-only prediction on binary catalyst accuracy.

### Hypothesis 2: Temporal graph beats analyst

The temporal-graph prediction outperforms Shkreli's call on the same catalysts.

### Hypothesis 3: Vol mispricing

Companies diagnosed with broken read_outcomes exhibit higher realized-to-implied vol ratios around catalyst dates than companies with functional read_outcomes.

## Sample

### What counts as a "position"

A position is a single Shkreli public statement that satisfies ALL of:
1. **Timestamped**: has a verifiable publication date
2. **Directional**: explicitly long, short, bull, bear, or states an outcome prediction ("will work", "will fail", "price target $X")
3. **Biotech-specific**: names a specific ticker or company in the biotech/pharma sector
4. **First occurrence**: if Shkreli makes multiple statements about the same ticker, the first directional statement is the position. Subsequent statements are reinforcements unless they reverse direction, in which case the reversal becomes a new position.

A position is NOT:
- Vague commentary ("interesting company", "watching this")
- Retweets or quote-tweets without added directional content
- Non-biotech calls (tech, crypto, quantum computing)

### Deduplication

One position per ticker per directional stance. If Shkreli is bull on SPRB in October and still bull in December, that's one position (October). If he flips from bull to bear, the bear statement is a second position with its own catalyst.

### Phase 1 discovery

Search Shkreli's public record (X/Twitter archive, YouTube, interviews, financial media coverage) from May 2022 through December 2025. The full list of qualifying positions is frozen before any diagnosis begins. Process all of them — no subset selection.

**Canonical source priority** (for the same position):
1. X/Twitter post with timestamp (preferred — most precise dating)
2. YouTube video with timestamp (second — verifiable but harder to quote)
3. Interview or article quoting Shkreli with publication date (third)
4. Financial media reporting his position (last resort)

### Inclusion criteria
- Qualifies as a position (per rules above)
- Company has a binary catalyst within 12 months of the position (trial readout, FDA action, regulatory filing)
- At least 3 dated public records exist before the catalyst
- Catalyst has resolved (Phase 1) or will resolve within 12 months (Phase 2)
- Listed options available at time of catalyst (Hypothesis 3 only)

### Exclusion criteria
- Fails position definition
- Companies with fewer than 3 dated public records before catalyst
- Catalysts that are ambiguous (no clear binary outcome determinable from a single public source)

### Analyst-to-catalyst mapping

When Shkreli's position is ticker-level (bull/bear on the company) rather than catalyst-specific:

1. If the company has exactly one upcoming binary catalyst within 12 months, map to that catalyst.
2. If the company has multiple upcoming catalysts, map to the **nearest** binary catalyst after Shkreli's position date.
3. If no binary catalyst exists within 12 months, exclude the position.
4. Shkreli bull → PASS on the mapped catalyst. Shkreli bear → FAIL on the mapped catalyst. Neutral → exclude.

### Eviction policy (Phase 2 only)

- **Resolved**: catalyst occurred, all three arms scored. Company moves to historical.
- **Voided**: catalyst window expired with no binary event. All three arms voided. Not counted in accuracy.
- **Dead**: company acquired, delisted, or entered bankruptcy. All three arms voided.

No stale eviction. Once a catalyst window is defined, it runs to completion regardless of whether Shkreli keeps commenting. The eviction applies to the prediction, not the company — if Shkreli takes a new position on the same company with a new catalyst, that's a new entry.

### Expected sample size
- **Phase 1**: estimated 20-30 qualifying positions with resolved catalysts.
- **Phase 2**: 5-10 new positions per year.

## Snapshot classification table

The snapshot-only arm uses the latest status per pipe (most recent event, ignoring temporal ordering) and classifies mechanically:

| Cache stack (4 pipes) | Consolidate stack (3 pipes) | Category | Direction |
|---|---|---|---|
| All functional/repaired | All functional/repaired | living_well | PASS |
| All functional/repaired | Any broken or stressed | living_dying | FAIL |
| Any broken or stressed | All functional/repaired | dying_pivoted | PASS |
| Any broken or stressed | Any broken or stressed | dying_dying | FAIL |

If a pipe has no events, it is treated as "unknown" which counts as neither functional nor broken — it is excluded from the count. If all pipes in a stack are unknown, that stack is treated as functional (benefit of the doubt — no evidence of breakage).

This table is exhaustive. No "etc." No judgment.

## Data sources

All public, all free or cheap:
- **ClinicalTrials.gov API**: trial designs, endpoints, results, amendments, posting dates
- **SEC EDGAR**: 10-K, 10-Q, 8-K filings with filing dates
- **PubMed**: published trial results with publication dates
- **FDA databases**: approval letters, CRLs, meeting minutes with issuance dates
- **CRSP / Yahoo Finance**: daily stock prices around catalyst dates
- **CBOE / OptionMetrics**: 30-day implied volatility before catalyst (Hypothesis 3; may require paid data)
- **Shkreli's public posts**: X (Twitter), YouTube, Substack, interviews — with timestamps and URLs

## Method

### For each qualifying position:

1. **Record the analyst call**: Shkreli's post URL, date, direction (bull/bear), mapped catalyst (per mapping rules above), PASS/FAIL.

2. **Define the catalyst**: exact event, resolution source, window, pass condition. Lock before any diagnosis.

3. **Build temporal graph** from public records dated before the catalyst. Each record is an event with: pipe, source_date, status, evidence, source_url.

4. **Generate temporal prediction**: 4 search agents, top-2 selection, 2 merge instances, soap-a default. Category from trajectory. Direction from category.

5. **Generate snapshot-only prediction**: same events, ignore ordering, latest status per pipe, classify per snapshot table above. Direction from table.

6. **Compute graph features**: recurrence count, transition count, repair latency, pipe coverage, event density, failure-to-repair path.

7. **Record confidence**: high/medium/low for temporal (merge agreement), inferred for analyst (language strength).

8. **Publish all three predictions** before catalyst date (Phase 2) or before scoring begins (Phase 1, with the full position list frozen first).

9. **Score**: check resolution source on window_end. All three arms scored against the same ground truth, same catalyst, same binary outcome.

10. **For Hypothesis 3**: Pull 30-day implied vol before catalyst, compute 5-day realized vol around catalyst. Ratio. Tag by read_outcomes status.

## Schema changes needed

The `prediction` table needs an `arm` field to support three predictions per company-catalyst:

```sql
ALTER TABLE prediction ADD COLUMN arm TEXT NOT NULL DEFAULT 'temporal'
    CHECK(arm IN ('temporal', 'snapshot', 'analyst'));
```

Unique constraint: `UNIQUE(company_id, arm, catalyst)` — one prediction per arm per catalyst.

The scorecard view and export must be updated to show all three arms side by side.

## Graph-derived features (collected at prediction time)

For each company at the moment of prediction, compute and store:
- **Recurrence count**: number of pipes where the same failure class appeared more than once
- **Transition count**: total status changes across all pipes
- **Repair latency**: days from most recent break event to most recent repair event (per pipe)
- **Days since last event**: staleness of the temporal graph
- **Pipe coverage**: fraction of seven pipes with at least one event (0-1)
- **Failure-to-repair path**: boolean — does at least one pipe show a broken → repaired trajectory?
- **Event density**: total events / months of coverage

## Confidence

Each prediction records a confidence level:
- **Framework confidence**: high / medium / low
  - High: both merges agree, strong trajectory signal, no ambiguous pipes
  - Medium: merges disagree (soap-a default), or trajectory mixed
  - Low: sparse events, multiple unknown pipes, trajectory unclear
- **Analyst confidence**: inferred from Shkreli's language
  - High: explicit position with price target or strong language
  - Medium: directional lean without conviction
  - Low: hedged or conditional

## Audit trail

Every prediction must have a complete chain:

1. **Shkreli source**: URL + archive of his public position with timestamp
2. **Search reports**: 4 agent outputs saved to `searches/{TICKER}/`
3. **SOAP notes**: 2 merge outputs saved to `notes/{TICKER}/`
4. **Diagnosis**: prediction records saved to `diagnoses/{TICKER}.md`
5. **DB records**: three rows in `prediction` table (temporal, snapshot, analyst) with `published_at` set
6. **Ground truth**: URL to the press release or 8-K that resolves the catalyst

## Scoring

### Hypothesis 1: Temporal beats snapshot
- **Primary metric**: temporal accuracy vs. snapshot-only accuracy on the same catalysts
- **Statistical test**: McNemar's test (paired binary outcomes)
- **This is the core test**

### Hypothesis 2: Temporal beats analyst
- **Primary metric**: temporal accuracy vs. Shkreli accuracy on the same catalysts
- **Secondary**: both vs. naive base rate (50%)
- **Statistical test**: McNemar's test (paired)

### Hypothesis 3: Vol mispricing
- **Primary metric**: mean realized/implied vol ratio, segmented by read_outcomes status
- **Minimum group size**: 5 per group
- **Tertiary** — may never reach power

## Known biases

1. **Selection bias**: only Shkreli's picks. Skews toward controversial, high-volatility names.
2. **Look-ahead bias (Phase 1)**: we know outcomes. Mitigated by: archival-date enforcement, snapshot-only arm as control (same bias applies to both arms equally).
3. **Classification bias**: framework author runs the diagnosis. Mitigated by: mechanical scoring, snapshot classification table, audit trail.
4. **Hindsight in Phase 1**: mitigated by freezing the full position list before any diagnosis.
5. **Small N**: Phase 1 gives N=20-30, borderline for McNemar's. Phase 2 adds power.
6. **LLM knowledge contamination (Phase 1)**: agents may know outcomes from training data. Affects all arms equally, so temporal-vs-snapshot comparison remains valid.

## Success criterion

**Descriptive**: all three arms reported side by side after each resolution. No inferential claim until N >= 20.

**Inferential** (if N reaches 20+):
- H1: temporal > snapshot at p < 0.05 (McNemar's)
- H2: temporal > analyst at p < 0.05 (McNemar's)
- Either can succeed or fail independently.

**Vol hypothesis**: descriptive at any N. Inferential only if both groups reach N >= 10.

**Exploratory (post-hoc, not pre-registered as primary)**:
- Among companies classified living_dying, do those with runway > 8 quarters hit more often than those with runway < 4 quarters? The hypothesis: given enough cash, a learning company will eventually outperform — the cash buys time for the consolidate stack to repair.
- Which bucket has the highest hit rate? The framework predicts dying_pivoted → PASS and dying_dying → FAIL, but the relative accuracy of living_well and living_dying is unknown.
- Do graph-derived features (recurrence count, repair latency, pipe coverage) predict accuracy within buckets?

These analyses require N=30+ with sufficient representation in each bucket. Deferred until Phase 1 data is complete.

## Commitment

- Process every qualifying Shkreli position (no cherry-picking)
- Publish all three arms before catalyst date (Phase 2) or before first scoring (Phase 1)
- Publish all outcomes regardless of result
- Maintain complete audit trail
- Update dashboard after each resolution
- Report misses at same prominence as hits

## Cost estimate

Per company: ~$0.50-1.50 in LLM API calls (4 agents + 2 merges). Phase 1 (25 companies): ~$25-40. Phase 2: $5-15/year.
