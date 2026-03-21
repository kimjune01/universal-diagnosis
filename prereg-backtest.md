# Pre-registration: Backtest

**Status**: Not started. Logged as future work.

## Research question

Does the Natural Framework's consolidate stack diagnosis predict Phase 3 binary outcomes better than the naive base rate, and do companies with broken read_outcomes pipes exhibit higher realized-to-implied volatility ratios around catalyst dates?

## Design

Retrospective backtest across public biotech Phase 3 readouts from 2020-2025.

### Hypothesis 1: Directional prediction

The framework's trajectory category (living_well, living_dying, dying_pivoted, dying_dying) predicts Phase 3 outcome (primary endpoint met or not) better than the historical base rate (~50% for Phase 3, per BIO/Informa).

- living_well → PASS
- dying_pivoted → PASS
- living_dying → FAIL
- dying_dying → FAIL

### Hypothesis 2: Vol mispricing

Companies diagnosed with broken read_outcomes (management overframing pattern) have higher realized-to-implied vol ratios around catalyst dates than companies with functional read_outcomes.

## Sample

### Inclusion criteria
- Public U.S. biotech company (SEC filings available)
- Phase 3 topline readout between January 1, 2020 and December 31, 2025
- Primary endpoint result publicly disclosed via press release or 8-K
- At least two prior trials or FDA interactions on the same program (enough history for temporal graph)
- Listed options available at time of readout (Hypothesis 2 only)

### Exclusion criteria
- Companies with fewer than 3 dated public records before the readout (insufficient temporal graph)
- Readouts where the primary endpoint result is ambiguous (e.g., mixed results with no clear met/not-met determination)

### Expected sample size
BIO/Informa reports ~1,500 Phase 3 trials initiated annually across all sponsors. Filtering to public U.S. companies with sufficient history and options data: estimated 200-400 scorable events over 2020-2025.

## Data sources

All public, all free or cheap:
- **ClinicalTrials.gov API**: trial designs, endpoints, results, amendments, posting dates
- **SEC EDGAR**: 10-K, 10-Q, 8-K filings with filing dates
- **PubMed**: published trial results with publication dates
- **FDA databases**: approval letters, CRLs, meeting minutes with issuance dates
- **CRSP / Yahoo Finance**: daily stock prices around catalyst dates
- **CBOE / OptionMetrics**: 30-day implied volatility before catalyst (Hypothesis 2; may require paid data)

## Method

### For each company-readout pair:

1. **Build temporal graph** from public records dated before the readout. Each record is an event with: pipe, source_date, status, evidence, source_url. Same schema as the pilot.

2. **Classify trajectory** using the same agent protocol as the pilot: 4 search agents, top-2 selection, 2 merge instances, soap-a default on disagreement. Category assigned: living_well, living_dying, dying_pivoted, dying_dying.

3. **Map category to direction**: living_well/dying_pivoted → PASS, living_dying/dying_dying → FAIL.

4. **Score against ground truth**: Did the Phase 3 primary endpoint meet statistical significance? Source: company press release or 8-K announcing topline. Binary: met or not met.

5. **For Hypothesis 2**: Pull 30-day implied vol before readout date, compute 5-day realized vol around readout date. Compute ratio. Tag company with read_outcomes status from the temporal graph.

### Automation

The pilot ran 4 agents per company manually. At 200-400 companies, this needs automation:
- Batch agent dispatch with structured prompts
- Automated event extraction from SEC EDGAR API and ClinicalTrials.gov API
- Automated category classification (may require a lighter model or rule-based classifier trained on pilot data)
- Cost estimate needed before starting

## Scoring

### Hypothesis 1
- **Primary metric**: accuracy (% correct PASS/FAIL predictions)
- **Benchmark**: BIO/Informa historical Phase 3 success rate for the same therapeutic areas
- **Statistical test**: binomial test against base rate. At N=300 and 55% accuracy vs. 50% base rate, power is ~80%.
- **Significance threshold**: p < 0.05

### Hypothesis 2
- **Primary metric**: mean realized/implied vol ratio, segmented by read_outcomes status
- **Statistical test**: two-sample t-test or Mann-Whitney U (depending on distribution)
- **Significance threshold**: p < 0.05
- **Minimum group size**: 30 companies per group (broken vs. functional read_outcomes)

## Known biases

1. **Survivorship bias**: only companies with listed options and sufficient public records are included. Smaller, less-covered companies are excluded.
2. **Look-ahead bias**: temporal graph must be built strictly from records dated before the readout. Any record with a source_date after the readout is excluded. This is enforceable because every event has an archival date.
3. **Classification bias**: the same framework that generated the pilot predictions classifies the backtest. No independent validation of the category assignments. Mitigated by mechanical scoring of outcomes.
4. **Agent drift**: LLM behavior may differ between pilot (2026) and backtest (analyzing 2020-2025 events). Model version should be locked.
5. **Endpoint ambiguity**: some Phase 3 readouts have ambiguous results (met secondary but not primary, met in subgroup, etc.). Strict rule: score against pre-specified primary endpoint only. If the company changed the primary endpoint mid-trial, use the last registered primary before readout.

## Success criterion

**Hypothesis 1**: Framework accuracy > base rate at p < 0.05. If the framework classifies at 55%+ on 300+ events, the consolidate stack diagnosis adds predictive power.

**Hypothesis 2**: Broken read_outcomes group has significantly higher realized/implied vol ratio than functional group at p < 0.05. Effect size > 0.2 (small-to-medium).

Either hypothesis can succeed or fail independently.

## Commitment

- Pre-register before running any backtest
- Lock model versions, prompts, and classification rules before processing any company
- Publish all results regardless of outcome
- Report accuracy, base rate, p-values, and effect sizes
- Release the full dataset (temporal graphs, classifications, outcomes) for replication

## Cost estimate

TBD. Main costs:
- LLM API calls for agent dispatch (~4 agents × 2 merges × 300 companies = ~1,800 calls)
- OptionMetrics or equivalent for historical IV data (may be $500-2,000)
- Compute time for batch processing
