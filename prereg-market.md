# Pre-registration: Framework vs. Market

**Status**: Draft. Not ready to execute. Six codex-identified blockers remain (see bottom). Depends on Phase 2 resolution, options data availability, and fixing the statistical design.

## Research question

Does the Natural Framework's consolidate stack diagnosis predict catalyst surprises — outcomes the market didn't price — better than chance?

## Key distinction from the Shkreli prereg

The Shkreli prereg asks: does the framework beat one analyst? This prereg asks: does the framework beat the market's collective expectation?

- Shkreli comparison: framework direction vs. one expert's direction
- Market comparison: framework diagnosis vs. market-implied probability

## Hypotheses

### H1: Direction — framework beats market-implied probability

The market prices a probability of success into the stock before each catalyst. The framework makes a binary PASS/FAIL prediction. If the framework's hit rate exceeds the market's implied accuracy, the framework sees directional information the market doesn't.

Market-implied probability: estimated from pre-catalyst stock price relative to post-catalyst scenarios (binary event pricing) or from options skew if available.

### H2: Vol — broken read_outcomes predicts higher surprise

Companies diagnosed with broken read_outcomes pipes (management overframing pattern) exhibit higher realized-to-implied volatility ratios around catalyst dates than companies with functional read_outcomes. The market underprices surprise because it calibrates to management's framing.

## Design

For each company-catalyst pair in the scorecard (Phase 1 + Phase 2):

### H1 data collection (direction)
1. **Before the catalyst**: estimate market-implied probability of success. Methods (use best available):
   - Binary event pricing: `P(success) = (current price - fail price) / (success price - fail price)` using analyst price targets or historical move-on-miss as the fail scenario
   - Options-implied: if binary options or tight-expiry straddles exist, derive implied probability from put/call pricing
2. **After the catalyst**: record actual outcome (PASS/FAIL)
3. **Score**: framework prediction vs. market-implied direction (was market pricing >50% success or <50%?)

### H2 data collection (vol)
1. **Before the catalyst**: pull 30-day implied volatility from listed options
2. **After the catalyst**: compute 5-day realized volatility around the event
3. **Compute**: realized/implied ratio
4. **Segment**: by read_outcomes status (broken vs. functional)
5. **Test**: do broken read_outcomes companies have higher ratios?

### What "beating the market" means

**On direction**: the framework predicts PASS or FAIL. The market prices a probability. If the framework is right more often than the market's implied probability, it has directional edge.

**On vol**: the framework predicts which companies will surprise. A broken read_outcomes pipe means management framing is unreliable, so the market's expectation is miscalibrated. The realized move will be larger than priced.

## Sample

Every company-catalyst pair from:
- Phase 1 backtest (CAPR, QURE, SAVA) — historical options data needed
- Phase 2 ongoing (SPRB, ATYR, INMB + future) — options data collected in real time
- Must have listed options with sufficient liquidity at time of catalyst

## Data needed

| Field | Source | Cost |
|-------|--------|------|
| 30-day implied vol before catalyst | OptionMetrics, CBOE, or broker API | Potentially $500-2,000 for historical |
| Daily closing prices around catalyst | Yahoo Finance / CRSP | Free |
| 5-day realized vol | Computed from daily closes | Free |
| read_outcomes status | From existing framework diagnosis | Free |

## Scoring

### H1: Direction
- **Primary metric**: framework accuracy vs. market-implied accuracy on the same catalysts
- **Market-implied accuracy**: if market priced >50% success and catalyst succeeded, market was "right" (and vice versa)
- **Statistical test**: McNemar's test (paired, same as Shkreli comparison)
- **Minimum N**: 10 before reporting

### H2: Vol
- **Primary metric**: mean realized/implied vol ratio, segmented by read_outcomes status (broken vs. functional)
- **Statistical test**: two-sample t-test or Mann-Whitney U
- **Minimum group size**: 5 per group before reporting
- **Significance threshold**: p < 0.05 for both

## Predictions from Phase 1

| Company | read_outcomes | Catalyst surprise? | Expected vol ratio |
|---------|--------------|--------------------|--------------------|
| CAPR | broken (spin on HOPE-2) | Yes — CRL after "no deficiencies" | High (realized > implied) |
| QURE | broken (fought FDA feedback) | Yes — FDA reversed agreement, stock -84% | High |
| SAVA | broken (defended fraud for 3 years) | Yes — Phase 3 failed after "stand behind science" | High |
| SPRB | functional | TBD | Lower expected |
| ATYR | functional | TBD | Lower expected |
| INMB | stressed | TBD | Medium expected |

All three Phase 1 companies had broken read_outcomes and large catalyst surprises. If the Phase 2 companies with functional read_outcomes show lower realized/implied ratios, the pattern holds.

## Known biases

1. **Small N**: Phase 1 has only 3 companies. Phase 2 adds 3 more. N=6 is underpowered for a two-group comparison.
2. **Biotech vol is inherently high**: all biotech catalyst dates produce high realized vol. The question is whether broken read_outcomes produces *higher* ratios, not whether biotech is volatile.
3. **Non-independent observations**: all companies are from Shkreli's positions, which skew toward controversial names. May not generalize.
4. **Options liquidity**: small-cap biotech options may be illiquid, making IV unreliable.

## Relationship to other preregs

- **Shkreli prereg**: tests framework vs. expert on binary outcomes (direction)
- **Market prereg**: tests framework vs. collective market on surprise magnitude (vol)
- Same companies, same diagnoses, different dependent variables
- A framework that beats Shkreli on direction AND predicts vol mispricing would be strong evidence that the consolidate stack diagnosis captures real information asymmetry

## Success criterion

**H1 (direction)**: framework accuracy > market-implied accuracy at p < 0.05. Descriptive until N >= 10.

**H2 (vol)**: broken read_outcomes group has higher realized/implied ratio than functional group at p < 0.05. Descriptive until N >= 5 per group.

**Practical significance**: if the framework beats the market on direction AND identifies vol mispricing, it captures information asymmetry on two independent dimensions. Either hypothesis can succeed or fail independently.

## Commitment

- Collect options data for every company in the scorecard
- Report ratios regardless of direction
- Acknowledge if the pattern doesn't hold
- Do not trade on this until the backtest confirms the pattern (this is research, not advice)

## Outstanding blockers (codex review, March 20 2026)

1. **H1 statistical design broken**: comparing binary framework call to market probability via McNemar doesn't work. Need Brier score or redefine H1 as pure sign classification.
2. **Market benchmark too discretionary**: "use best available" allows method shopping. Need one locked estimator, one formula, one timestamp.
3. **H2 horizon mismatch**: 30-day IV vs 5-day realized vol aren't comparable. Need event-window implied move (nearest expiry ATM straddle) vs realized absolute return.
4. **H2 grouping variable not operationalized**: broken/functional binary doesn't account for stressed/repaired/unknown/mixed. Need a locked mapping rule.
5. **Catalyst definitions inconsistent across files**: QURE treated as topline in backtest prereg but as FDA reversal in market prereg. Must lock to one event.
6. **H2 sample too small for confirmatory test**: all Phase 1 companies have broken read_outcomes. Need functional-read_outcomes companies for comparison. Label H2 as exploratory until sample grows.
