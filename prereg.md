# Pre-registration: Biotech Pilot

## Research question

Can the Natural Framework's recursive pipe diagnosis generate non-obvious predictions about biotech company outcomes that match or exceed domain expert (analyst) accuracy?

## Design

- **Run 0** (retrospective): 3-5 companies with known outcomes. Diagnose post hoc. Does the framework explain the outcome in a way that adds to the analyst narrative?
- **Run 1** (prospective): 3-5 companies with upcoming catalyst dates. Diagnose, predict, publish before the date. Score against analyst consensus.

## Target selection

Targets are drawn from Martin Shkreli's public biotech positions (2025-2026). Shkreli is chosen because:
- Named, public, timestamped calls with clear bull/bear positions
- High-profile enough that head-to-head comparison is attention-worthy
- Has a documented miss (CAPR) and active forward positions (SPRB, ATYR, INMB)

Seeded companies: CAPR, SPRB, QURE, ATYR, INMB.

## Inclusion criteria

- Public biotech company (SEC filings available)
- At least two trials or FDA interactions on the same program (enough history for recurrence probes)
- Upcoming catalyst within 6 months (Run 1 only)
- Named analyst coverage exists for head-to-head comparison

## Methods

### Diagnosis process
1. Identify the molecule-as-pipe: compound, target, mechanism, indication
2. Map the company to the consolidate stack: who reads outcomes (clinical ops), who processes them (R&D), who writes back to substrate (manufacturing, regulatory)
3. Run the stack-level probe: is the forward pass broken (wrong output now), or is the backward pass broken (hasn't improved over time)?
4. Check for trauma recurrence: find known failures, check if the same class recurred
5. Classify prediction type: recurrence, cascade, fix, death, or mitosis
6. Record analyst position for head-to-head

### Tools
- SQLite database with relational schema (companies, recursive pipe tree, traumas, predictions, analyst calls)
- Sentence embeddings (all-MiniLM-L6-v2) for semantic matching of trauma descriptions and pipe descriptions
- Cosine similarity threshold (0.6) for recurrence probe: "is this failure similar to a prior failure?"
- Public data sources: ClinicalTrials.gov, FDA databases, SEC EDGAR, PubMed

### The consolidate heuristic
The cheap probe for diagnosing the backward pass: instead of "is this company learning?" (expensive), ask "has this company repeated a known failure?" (cheap event matching). `count(similar_failures) > 1` = broken consolidate. Similarity is measured via embedding cosine similarity on failure descriptions.

## Predictions per company

Each diagnosis produces exactly one primary prediction, classified by type (recurrence, cascade, fix, death, mitosis). Secondary predictions allowed but scored separately.

## Scoring

- **Hit**: predicted event occurs within stated timeframe
- **Miss**: predicted event does not occur, or opposite occurs
- **Void**: catalyst is delayed or company is acquired/merged before the date (removed from scorecard, not counted as hit or miss)

## Commitment

- Publish all predictions before catalyst dates
- Publish all outcomes regardless of result
- Do not revise predictions after publication
- Report hit rate, miss rate, and void rate separately
- Compare framework hit rate to analyst consensus hit rate on the same catalysts

## Success criterion

Run 0: The framework produces at least one explanation that is structurally distinct from the analyst narrative (not just rewording the same insight in different vocabulary).

Run 1: Framework hit rate ≥ analyst consensus hit rate on the same catalysts, OR at least one hit where consensus was wrong. N is small, so statistical significance is not the goal — the goal is one credible proof of concept.

## Known biases

1. **Selection bias**: Targets are chosen from one analyst's positions, not randomly sampled. Shkreli's picks skew toward controversial, high-volatility names. Mitigated by pre-registering all seeded companies and diagnosing all of them, not cherry-picking.

2. **Confirmation bias**: The diagnostician (us) created the framework and wants it to succeed. We will see what we want to see. Mitigated by:
   - Publishing the diagnosis before the catalyst date (no post-hoc fitting)
   - Using a mechanical heuristic (trauma recurrence via embedding similarity) rather than subjective judgment where possible
   - Publishing misses at the same prominence as hits

3. **Hindsight bias** (Run 0 only): Retrospective diagnoses inevitably benefit from knowing the outcome. Mitigated by focusing on whether the framework's *explanation* is structurally distinct, not just whether it arrives at the correct answer.

4. **Domain naivety**: We are not biotech domain experts. We may misidentify which organizational function maps to which stack stage, or miss domain-specific context that would change the diagnosis. Mitigated by using only public, verifiable data sources and documenting the mapping explicitly so others can critique it.

5. **Small N**: 3-5 companies per run is not statistically powered. A lucky streak is indistinguishable from a working framework at this sample size. This is a pilot — the goal is proof of concept, not proof.

6. **Survivorship bias in trauma data**: We can only check for recurrence of *known* failures. Companies may have unreported failures, or failures that don't appear in public records. The recurrence probe only works on documented traumas.

7. **Embedding model limitations**: all-MiniLM-L6-v2 may not capture biotech-specific semantic similarity well. Two failures that a domain expert would recognize as the same class might have low cosine similarity if described in different clinical language. May need domain-specific embedding or manual category labels as fallback.

## Limitations

- Small N. This is a pilot, not a powered study.
- Selection bias in company choice. Mitigated by pre-registering selections before diagnosis.
- The diagnostician (us) is not blind to analyst consensus. Mitigated by publishing the framework diagnosis before looking up analyst positions where possible.
- "Non-obvious" is subjective. Mitigated by publishing both the framework's reasoning and the analyst's, letting readers judge.
- We are predicting process (will the company iterate effectively?), not product (will the drug work?). If the drug fails for biological reasons unrelated to the company's learning loop, the framework's prediction is void, not wrong. This distinction must be stated clearly in each prediction.
