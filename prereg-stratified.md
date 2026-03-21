# Pre-registration: Stratified Biotech Backtest

**Status**: Draft. Designing.

## Research question

Does the Natural Framework's consolidate stack diagnosis predict biotech catalyst outcomes better than market expectations, and does the signal strength vary with company hype/popularity?

## Key distinction from other preregs

- **Shkreli prereg**: follows one analyst's picks (biased sample, small N)
- **Market prereg**: tests vol mispricing on the Shkreli sample (underpowered)
- **This prereg**: stratified random sample from the population of biotech catalysts, balanced success/failure, ranked by hype

## Design

Retrospective backtest on biotech Phase 3 readouts from 2020-2025.

### Sample construction

1. **Pull the population**: every biotech Phase 3 topline readout from 2020-2025 with a binary outcome (primary endpoint met or not met). Source: ClinicalTrials.gov results postings + company press releases.

2. **Stratify by outcome**: equal numbers of successes and failures. If there are 200 successes and 150 failures, sample 100 from each. This ensures balanced classes and prevents the framework from gaming by always predicting one direction.

3. **Rank by hype/popularity**: for each company-catalyst, compute a hype score from:
   - Pre-catalyst social media mention volume (StockTwits, Reddit r/wallstreetbets, X)
   - Number of sell-side analyst reports covering the company
   - Average daily trading volume in the 30 days before catalyst
   - Retail ownership percentage (if available from 13F filings)

   Normalize to a 0-1 scale. High hype = management framing reaches more people = more opportunity for read_outcomes distortion to matter.

4. **Sample within hype strata**: equal numbers from high-hype and low-hype terciles. This ensures we test whether the framework adds more signal for famous stocks than obscure ones.

### Final sample: 2×2 balanced

| | Success | Failure |
|---|---|---|
| **High hype** | N/4 | N/4 |
| **Low hype** | N/4 | N/4 |

Target N = 100 (25 per cell). Large enough for logistic regression with interaction terms.

## Hypotheses

### H1: Framework predicts direction better than base rate

Framework accuracy > 50% on the balanced sample. Since the sample is 50/50 success/failure by construction, base rate is exactly 50%.

- **Statistical test**: binomial test, then logistic regression with framework prediction as predictor of outcome
- **Significance**: p < 0.05

### H2: Framework adds more signal for high-hype stocks

Interaction effect: framework accuracy is higher in the high-hype stratum than the low-hype stratum.

- **Rationale**: high-hype companies have louder management framing. If the framework's value is diagnosing distorted read_outcomes, it should matter more when the framing reaches more people.
- **Statistical test**: logistic regression with hype × framework_prediction interaction
- **Significance**: interaction term p < 0.05

### H3: Broken read_outcomes predicts larger surprises

Among companies the framework diagnoses with broken read_outcomes, the market-implied expected move underestimates the realized move.

- **Measure**: |realized return over event window| vs. implied move from nearest-expiry ATM straddle price
- **Statistical test**: paired t-test (realized vs implied) within broken read_outcomes group
- **Significance**: p < 0.05
- **This is the vol hypothesis, properly specified**

## Hype score specification

Computed per company at T-30 days before catalyst. Locked formula:

```
hype_score = 0.4 * norm(social_mentions) + 0.3 * norm(analyst_count) + 0.3 * norm(avg_daily_volume)
```

Where `norm()` is min-max normalization across the full population. Weights chosen a priori, not tuned.

Social mentions: count of ticker mentions on StockTwits + Reddit in the 30-day window before catalyst. Source: Quiver Quant or similar API.

Analyst count: number of unique sell-side analysts with published price targets. Source: TipRanks or Yahoo Finance.

Volume: average daily trading volume in shares. Source: Yahoo Finance.

## Method

### For each company in the sample:

1. **Build temporal graph** from public records dated before the catalyst. Same 7-pipe schema, same agent protocol (4 agents, top-2, 2 merges, soap-a default).

2. **Generate temporal prediction**: category + direction.

3. **Generate snapshot-only prediction**: latest status per pipe, snapshot classification table.

4. **Record market expectation**: implied move from nearest-expiry ATM straddle (for H3), plus any available market-implied success probability.

5. **Compute hype score** at T-30.

6. **Score against ground truth**: primary endpoint met or not, from ClinicalTrials.gov or company press release.

### Automation required

N=100 requires batch processing. Per company: ~$0.50-1.50 in API calls. Total: ~$50-150. The agents process independently, one company at a time, results append to the DB as they complete. Dashboard shows convergence in real time.

## Data sources

- **ClinicalTrials.gov API**: population of Phase 3 readouts with results
- **SEC EDGAR**: company filings for temporal graph events
- **PubMed**: published trial results
- **Yahoo Finance**: daily prices, trading volume
- **StockTwits / Reddit API**: social mention counts
- **TipRanks**: analyst coverage count
- **Options data (H3 only)**: nearest-expiry ATM straddle prices. Source TBD.

## Known biases

1. **Survivorship bias**: only companies with ClinicalTrials.gov results postings are included. Some failed trials may not post results promptly.
2. **Look-ahead bias**: outcomes are known. Temporal graphs must use only pre-catalyst records. LLM knowledge contamination affects all arms equally.
3. **Hype score is retrospective**: social mentions and volume data are historical. The score itself is not a prediction — it's a stratification variable.
4. **Balanced sample is artificial**: real biotech has ~50% Phase 3 success rate, so 50/50 balance roughly matches reality. But forced balance removes base-rate information.
5. **Options liquidity**: many small-cap biotechs have illiquid options. H3 sample may be smaller than N=100.

## Success criteria

**H1**: framework accuracy > 50% at p < 0.05 on balanced sample. At N=100, 59% accuracy gives p < 0.05 (binomial).

**H2**: hype × prediction interaction significant at p < 0.05 in logistic regression. This would mean the framework is more accurate on famous stocks — the structural prediction it makes.

**H3**: |realized return| > implied move for broken read_outcomes companies at p < 0.05 (paired t-test). This would mean the framework identifies vol mispricing.

Any can succeed or fail independently.

## Commitment

- Sample constructed and frozen before any diagnosis
- All companies in the sample processed — no cherry-picking
- Hype scores computed and locked before diagnosis
- All results published regardless of outcome
- Misses reported at same prominence as hits

## Cost estimate

- Agent calls: ~$50-150 for N=100
- Social mention data: StockTwits API free, Reddit API free tier
- Analyst data: TipRanks may require subscription (~$30/month)
- Options data: OptionMetrics ($500-2,000) or free from broker APIs for recent data
- Total: ~$600-2,300, mostly options data
