# Pre-registration: Framework vs. Market

**Status**: Draft. Depends on Phase 2 resolution and options data availability.

## Research question

Does the Natural Framework's consolidate stack diagnosis predict catalyst surprises — outcomes the market didn't price — better than chance?

## Key distinction from the Shkreli prereg

The Shkreli prereg asks: does the framework beat one analyst? This prereg asks: does the framework beat the market's collective expectation?

- Shkreli comparison: framework direction vs. one expert's direction
- Market comparison: framework diagnosis vs. market-implied probability

## Hypothesis

Companies diagnosed with broken read_outcomes pipes (management overframing pattern) exhibit higher realized-to-implied volatility ratios around catalyst dates than companies with functional read_outcomes. The market underprices surprise because it calibrates to management's framing.

## Design

For each company-catalyst pair already in the scorecard (Phase 1 + Phase 2):

1. **Before the catalyst**: pull 30-day implied volatility from listed options
2. **After the catalyst**: compute 5-day realized volatility around the event
3. **Compute**: realized/implied ratio
4. **Segment**: by read_outcomes status (broken vs. functional, from the framework's diagnosis)
5. **Test**: do broken read_outcomes companies have higher ratios?

## What "beating the market" means here

The framework doesn't predict stock direction. It predicts *surprise magnitude*. A company with broken read_outcomes has a wider gap between management's framing and reality. The market, calibrating to management's framing, underestimates the possible move. Realized vol > implied vol.

This is testable without taking directional positions. It's a statement about information quality, not stock price.

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

- **Primary metric**: mean realized/implied vol ratio, segmented by read_outcomes status (broken vs. functional)
- **Statistical test**: two-sample t-test or Mann-Whitney U
- **Minimum group size**: 5 per group before reporting
- **Significance threshold**: p < 0.05

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

**Descriptive**: report realized/implied ratios per company, segmented by read_outcomes status.

**Inferential** (if groups reach N >= 5 each): broken > functional at p < 0.05.

**Practical significance**: if broken read_outcomes companies average 2x+ realized/implied ratio while functional companies average < 1.5x, the framework identifies tradeable vol mispricing.

## Commitment

- Collect options data for every company in the scorecard
- Report ratios regardless of direction
- Acknowledge if the pattern doesn't hold
- Do not trade on this until the backtest confirms the pattern (this is research, not advice)
