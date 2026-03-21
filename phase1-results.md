# Phase 1 Results: Historical Backtest

**Date**: March 20, 2026
**N**: 3 (CAPR, QURE, SAVA)
**Status**: Descriptive only. N=3 is not inferential.

## Scorecard

| Company | Category | Framework | Shkreli | Outcome | Framework correct? | Shkreli correct? |
|---------|----------|-----------|---------|---------|-------------------|-----------------|
| CAPR | dying_pivoted | PASS | FAIL | PASS (HOPE-3 hit) | ✓ | ✗ |
| QURE | dying_dying | PASS (topline) | PASS | PASS (topline hit) | ✓ | ✓ |
| SAVA | dying_dying | FAIL | FAIL | FAIL (both Phase 3 missed) | ✓ | ✓ |

**Framework: 3/3 (100%)**
**Shkreli: 2/3 (67%)**
**Disagreement on: CAPR** — framework predicted PASS from trajectory (dying_pivoted), Shkreli predicted FAIL from snapshot (drug won't work). Framework was right.

## What Phase 1 showed

1. **The framework produced correct retrospective predictions on all three companies.** But this is a backtest with known outcomes and N=3 — descriptive, not proof.

2. **The one disagreement (CAPR) went the framework's way.** Shkreli diagnosed the forward pass (molecule snapshot). The framework diagnosed the backward pass (company trajectory). The trajectory was right.

3. **Where both agreed (SAVA, QURE), both were right.** Independent convergence from different analyses. SAVA: both saw the drug can't work (fabricated preclinical data). QURE: both saw the drug works (topline positive).

4. **Two trajectory categories appeared**: dying_pivoted (CAPR) and dying_dying (QURE, SAVA). Both predicted correctly. living_well and living_dying did not appear in the sample.

## What Phase 1 did NOT show

1. **Temporal vs. snapshot comparison not run.** The prereg requires a snapshot-only arm for each company. CAPR has a retroactive snapshot baseline (the smoke test), but QURE and SAVA do not. This is a gap — we cannot yet claim temporal ordering adds value over the snapshot classification table.

2. **No statistical significance.** N=3 cannot support McNemar's test or any inferential claim. Even 3/3 correct has p=0.125 against a 50% base rate (binomial).

3. **Look-ahead bias is real.** We knew the outcomes. The LLM agents may have latent knowledge of outcomes from training data. The snapshot-only arm would partially control for this (same bias in both arms), but it hasn't been run.

4. **Selection bias.** Three companies from one analyst's positions. Not representative of biotech broadly.

## Limitations

- Retrospective only. The real test is Phase 2 (prospective).
- Snapshot-only arm owes for QURE and SAVA.
- N too small for any statistical claim.
- Two of three were consensus calls (SAVA fail, QURE topline pass) — only CAPR was a non-obvious prediction.

## Next

- Phase 2 predictions are live (SPRB, ATYR, INMB). First resolution: Sep 30, 2026.
- Snapshot-only arm for QURE and SAVA should be run to complete the three-arm comparison.
- Market comparison prereg in development.
