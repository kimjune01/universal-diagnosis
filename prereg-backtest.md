# Pre-registration: Ongoing Scorecard

**Status**: Active. N grows as Shkreli takes public positions.

## Research question

Does the Natural Framework's consolidate stack diagnosis predict biotech catalyst outcomes better than Martin Shkreli's public calls on the same companies?

## Design

Follow Shkreli's public biotech positions as they appear. Each one gets the full treatment: 4 search agents, temporal graph, category classification, PASS/FAIL prediction, scored against ground truth. N grows organically.

### Hypothesis 1: Directional prediction

The framework's trajectory category predicts catalyst outcome better than Shkreli's call on the same catalyst.

### Hypothesis 2: Vol mispricing

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

6. **Publish prediction** before catalyst date. Commit to repo with timestamp.

7. **Score against ground truth**: check resolution source on window_end. Binary: pass condition met or not.

8. **For Hypothesis 2**: Pull 30-day implied vol before catalyst date, compute 5-day realized vol around catalyst. Compute ratio. Tag company with read_outcomes status.

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

### Hypothesis 1: Head-to-head
- **Primary metric**: framework accuracy vs. Shkreli accuracy on the same catalysts
- **Secondary**: framework accuracy vs. naive base rate (50% for Phase 3)
- **Statistical test**: binomial test. At N=10, 9/10 correct is p=0.01 vs 50% base rate. At N=10, even 8/10 is p=0.055.
- **Realistic expectation**: N will grow slowly. Statistical significance may take years. The dashboard shows convergence in real time.

### Hypothesis 2: Vol mispricing
- **Primary metric**: mean realized/implied vol ratio, segmented by read_outcomes status
- **Minimum group size**: 5 per group before computing (small N acknowledged)
- **This hypothesis is secondary** — it runs in parallel but may never reach statistical power with Shkreli-only sample

## Known biases

1. **Selection bias**: we only diagnose companies Shkreli covers. His picks skew toward controversial, high-volatility names. Not a random sample of biotech.
2. **Look-ahead bias**: temporal graph must be built strictly from records dated before the catalyst. Enforceable because every event has a source_date.
3. **Classification bias**: the framework author (us) also runs the diagnosis. Mitigated by mechanical scoring and audit trail.
4. **Small N**: significance accumulates slowly. The dashboard shows convergence but may never reach p < 0.05. That's a result, not a failure.

## Success criterion

**Descriptive**: framework accuracy and Shkreli accuracy reported side by side after each resolution. No inferential claim until N >= 20.

**Inferential** (if N reaches 20+): framework accuracy > Shkreli accuracy or > base rate at p < 0.05.

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
