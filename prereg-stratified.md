# Pre-registration: Stratified Biotech Backtest

**Status**: Draft. Iterating with codex.

## Research question

Does the Natural Framework's consolidate stack diagnosis predict biotech catalyst outcomes better than chance, and does the signal strength vary with company hype/popularity?

## Key distinction from other preregs

- **Shkreli prereg**: follows one analyst's picks (biased sample, small N)
- **This prereg**: stratified random sample from the population, balanced success/failure, ranked by hype

## Design

Retrospective backtest on biotech Phase 3 readouts from 2020-2025.

### Sample construction

#### Step 1: Enumerate the population

Source: ClinicalTrials.gov API. Query:
```
study_type = INTERVENTIONAL
phase = PHASE3
results_first_posted >= 2020-01-01
results_first_posted <= 2025-12-31
```

Filter to:
- **Biotech definition**: sponsor is a publicly traded U.S. company (has SEC CIK number) with market cap < $20B at time of readout. This excludes big pharma (Pfizer, Merck, etc.) where the consolidate stack dynamics are different.
- **Binary outcome**: primary endpoint has a clear met/not-met determination in the results posting or contemporaneous press release. Exclude trials where the primary endpoint result is ambiguous, mixed, or unreported.
- **One entry per company-catalyst**: if a company has multiple Phase 3 readouts, each is a separate entry. Deduplicate by NCT number.

#### Step 2: Label outcomes

For each trial in the population:
- **Success**: primary endpoint met statistical significance as pre-specified
- **Failure**: primary endpoint did not meet statistical significance

Source of truth: ClinicalTrials.gov results posting (primary outcome measure, p-value or CI). If results are not posted, use the company's press release or 8-K announcing topline (must be dated within 7 days of trial completion).

#### Step 3: Compute hype score

For each company-catalyst, at T-30 days before the results posting date:

```
hype_score = 0.4 * norm(social_mentions) + 0.3 * norm(analyst_count) + 0.3 * norm(avg_daily_volume)
```

- **social_mentions**: count of ticker mentions on StockTwits in the 30-day window before catalyst. Source: StockTwits API (free, historical data available). If StockTwits data unavailable for a company, use 0.
- **analyst_count**: number of unique sell-side analysts with published price targets at time of catalyst. Source: Yahoo Finance analyst page (count of analysts). If unavailable, use 0.
- **avg_daily_volume**: average daily trading volume in shares over the 30 days before catalyst. Source: Yahoo Finance historical data (free).
- **norm()**: min-max normalization across the full population.

Missing data rule: if 2 of 3 components are unavailable, exclude the company from hype stratification. Use the remaining companies for sampling.

#### Step 4: Stratify and sample

Split the population into:
- **High hype**: top tercile of hype_score
- **Low hype**: bottom tercile of hype_score
- Middle tercile excluded (reduces ambiguity)

Within each hype stratum, randomly sample equal numbers of successes and failures. Target: 25 per cell.

### Final sample: 2×2 balanced

| | Success | Failure |
|---|---|---|
| **High hype** | 25 | 25 |
| **Low hype** | 25 | 25 |

Total N = 100. Frozen before any diagnosis.

## Hypotheses

### H1: Framework predicts direction better than base rate

Framework accuracy > 50% on the balanced sample.

- **Statistical test**: binomial test (one-sided, H_a: p > 0.5)
- **Significance**: p < 0.05
- At N=100, need 59+ correct for significance

### H2: Framework adds more signal for high-hype stocks

Framework accuracy is higher in the high-hype stratum than the low-hype stratum.

- **Rationale**: high-hype companies have louder management framing. If the framework's value is diagnosing distorted read_outcomes, it should matter more when the framing reaches more people.
- **Statistical test**: logistic regression: `outcome ~ framework_prediction * hype_stratum`
- **Significance**: interaction term p < 0.05
- **Directional prediction**: framework accuracy higher in high-hype group

### H3: Broken read_outcomes predicts larger stock moves

Among companies the framework diagnoses with broken read_outcomes, the absolute stock price move on catalyst day is larger than among companies with functional read_outcomes.

- **Measure**: |close-to-close return on catalyst day| (or next trading day if announcement is after hours)
- **Statistical test**: two-sample t-test or Mann-Whitney U (broken vs functional groups)
- **Significance**: p < 0.05
- **No options data needed** — uses stock price only

### read_outcomes grouping rule (for H3)

The read_outcomes pipe has status per event. For each company, the latest read_outcomes event before the catalyst determines the group:
- **Broken**: latest read_outcomes status is `broken`
- **Functional**: latest read_outcomes status is `functional` or `repaired`
- **Exclude**: latest status is `stressed`, `unknown`, or no read_outcomes events exist

This is binary with exclusions. No ambiguity.

## Anti-contamination procedure (LLM knowledge leakage)

The LLM agents may have been trained on data that includes trial outcomes from 2020-2025. This is the primary validity threat for a retrospective backtest.

### Controls:

1. **Temporal graph enforcement**: every event must have a source_date before the catalyst. The agent prompt explicitly instructs: "Do NOT make predictions. Report events with dates." The evidence field and source_url are auditable — if an agent cites a post-catalyst source, that event is excluded.

2. **Snapshot-only arm as contamination control**: the snapshot arm uses the same LLM, same events, same potential contamination — but without temporal ordering. If contamination drives both arms equally, the temporal-vs-snapshot comparison remains valid. H1 (temporal > 50%) is vulnerable to contamination. The temporal-vs-snapshot delta is not.

3. **Post-hoc contamination audit**: after all diagnoses, randomly sample 20 companies and manually verify that no event has a source_date after the catalyst. If > 5% of events are post-catalyst, flag the entire run.

4. **Acknowledged limitation**: this is a retrospective backtest with known outcomes and modern LLMs. The primary defense is that contamination affects all arms equally, so relative comparisons (H2 interaction, temporal vs snapshot) are valid even if absolute accuracy (H1) is inflated.

## Diagnostic labels

The framework produces a category and direction per the locked rules:

### Temporal arm
- Category from agent diagnosis: living_well, living_dying, dying_pivoted, dying_dying
- Direction: living_well/dying_pivoted → PASS, living_dying/dying_dying → FAIL
- Process: 4 agents, top-2, 2 merges, soap-a default

### Snapshot arm
- Category from the snapshot classification table (from prereg-backtest.md):

| Cache stack (4 pipes) | Consolidate stack (3 pipes) | Category | Direction |
|---|---|---|---|
| All functional/repaired | All functional/repaired | living_well | PASS |
| All functional/repaired | Any broken or stressed | living_dying | FAIL |
| Any broken or stressed | All functional/repaired | dying_pivoted | PASS |
| Any broken or stressed | Any broken or stressed | dying_dying | FAIL |

Unknown pipes excluded from count. If all pipes in a stack are unknown, stack treated as functional.

Both arms produce PASS/FAIL from locked rules. No subjective judgment in the direction mapping.

## Data sources (locked)

- **Population**: ClinicalTrials.gov API (`/v2/studies` endpoint)
- **Outcome**: ClinicalTrials.gov results posting or company press release/8-K within 7 days
- **Temporal graph events**: SEC EDGAR, ClinicalTrials.gov, PubMed, FDA databases — same as pilot
- **Hype score**: StockTwits API (social mentions), Yahoo Finance (analyst count, daily volume)
- **Stock price**: Yahoo Finance historical daily closes (for H3)

## Method

### For each company in the sample:

1. **Build temporal graph** from public records dated before the catalyst. Same 7-pipe schema, same agent protocol.

2. **Generate temporal prediction**: category + direction per locked rules.

3. **Generate snapshot-only prediction**: latest status per pipe, snapshot classification table.

4. **Compute hype score** at T-30 (already computed during sampling — just record it).

5. **Score against ground truth**: primary endpoint met or not, from ClinicalTrials.gov.

6. **For H3**: record |close-to-close return| on catalyst day. Segment by read_outcomes status.

### Automation

N=100 in batch. Per company: ~$0.50-1.50 in API calls. Total: ~$50-150. Dashboard shows convergence in real time.

## Known biases

1. **Survivorship bias**: only trials with posted results included. Some failed trials delay posting.
2. **Look-ahead bias**: outcomes known. Mitigated by source_date enforcement + snapshot arm as contamination control.
3. **LLM contamination**: acknowledged, controlled (see anti-contamination procedure above).
4. **Hype score is retrospective**: stratification variable, not a prediction.
5. **Balanced sample is artificial**: roughly matches real Phase 3 success rate (~50%).

## Success criteria

**H1**: framework accuracy > 50% at p < 0.05 (binomial, N=100).

**H2**: hype × prediction interaction significant at p < 0.05 (logistic regression).

**H3**: |catalyst-day return| larger for broken read_outcomes than functional at p < 0.05 (two-sample test).

Any can succeed or fail independently.

## Commitment

- Sample constructed and frozen before any diagnosis
- All 100 companies processed — no cherry-picking
- Hype scores locked before diagnosis
- Contamination audit on 20 random companies
- All results published regardless of outcome
- Misses reported at same prominence as hits

## Cost estimate

- Agent calls: ~$50-150 for N=100
- StockTwits API: free
- Yahoo Finance: free
- Total: ~$50-150. No options data needed.
