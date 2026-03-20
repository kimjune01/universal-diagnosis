# Work Log

## 2026-03-20: Initial design session

Started exploring universal diagnosis as a cheap Attend alternative for agents. Key moves in the conversation:

1. **MCTS over a universal fault tree** — instead of blind-blind-merge (expensive portfolio solvers), use MCTS (implicit redundancy, same row in the Attend grid). The Natural Framework's six roles provide a portable tree structure that works across domains.

2. **Two stacks per node** — every pipe has a cache stack (forward pass, 4 handoffs) and a consolidate stack (backward pass, 3 stages). First diagnostic question at any node is which stack, a cheap binary split.

3. **Recursive structure** — no privileged scales. Every node is a pipe, every pipe has the same shape, recurse until rock bottom (atomic operation). Sector/domain/function are metadata for priors, not structural layers.

4. **Trauma recurrence heuristic** — cheap consolidate probe. Instead of "is this system learning?" (expensive), ask "has this system repeated a known failure?" (cheap event matching). Works at every scale.

5. **Goal reframe** — the tool isn't the product, the predictions are. Generate falsifiable predictions from the framework, publish them, build a scorecard. Mendeleev play: legitimize the framework by predicting what others can't.

6. **Five prediction types**: recurrence, cascade, fix, death, mitosis. Mitosis is the novel one — a stack that outgrows its parent pipe must split into an independent pipe or starve the sibling stack.

7. **Biotech as pilot sector** — data is public (ClinicalTrials.gov, FDA, SEC), outcomes are documented, market prices predictions fast. Key framing: the molecule is the pipe, the company is its consolidate stack. The entire org chart maps onto Read → Process → Write.

8. **Coordination protocol** — marketing-speak as the common language between agents and humans. Node descriptions are human-readable sentences that double as lock names.

9. **Head-to-head with analysts** — biotech analysts are named, public, and trackable. The legitimacy play is timestamped predictions that contradict specific analysts, scored honestly. The framework's edge: process prediction (will the company iterate effectively?) vs. outcome prediction (will the drug work?).

10. **Quarterly catalyst calendar** — biotech has pre-scheduled events (earnings, PDUFA dates, trial readouts). Publish before the date, outcome is public within days. Fastest possible scorecard iteration.

### Files created
- `README.md` — project overview
- `CLAUDE.md` — agent context
- `taxonomy.md` — recursive tree structure
- `probes.md` — diagnostic probes by stack and fault site
- `design.md` — full design doc with goal, prediction types, runs, coordination
- `biotech.md` — biotech pilot: org-chart mapping, prediction examples, data sources
- `worklog.md` — this file

## Methodology

### How to diagnose a biotech company

1. **Identify the molecule-as-pipe.** What compound is the company iterating on? What's the target, mechanism, indication? This is the forward pass — compound → binding → effect → outcome.

2. **Map the company to the consolidate stack.** Who reads outcomes (clinical ops, biostats)? Who processes them (R&D, med chem)? Who writes back to the substrate (manufacturing, formulation, regulatory)? Public sources: 10-K org descriptions, LinkedIn headcount by function, conference presentations.

3. **Run the stack-level probe.** Is the output wrong now (cache stack), or has it failed to improve over time (consolidate stack)? For biotech, "failed to improve" means: did the compound change meaningfully between trial iterations? Compare intervention descriptions on ClinicalTrials.gov across sequential trials.

4. **Check for trauma recurrence.** Find a known failure (trial miss, CRL, clinical hold). Check if the same class of failure recurred. Sources: FDA letters, trial results, SEC risk factor disclosures. `count(similar_failures) > 1` = broken consolidate.

5. **Classify the prediction type.**
   - Recurrence: same failure class will happen again (consolidate broken at batch process)
   - Cascade: too many similar candidates, one failure will correlate across pipeline (Filter → Attend handoff broken)
   - Fix: specific parts bin algorithm would address the gap
   - Death: multiple broken stages, loop can't self-correct
   - Mitosis: platform/infrastructure consuming disproportionate resources, will spin off or starve the pipeline

6. **Find the analyst consensus.** What are named analysts predicting for the same catalyst? Sources: analyst reports (sometimes paywalled), earnings call transcripts (free via SEC), financial media coverage, price targets.

7. **Publish the prediction.** Timestamped, with:
   - The framework's diagnosis (which stack, which stage, which type)
   - The specific falsifiable claim
   - The catalyst date (when the outcome will be known)
   - The analyst consensus or a named contrary position
   - The evidence trail (links to public sources)

8. **Score.** After the catalyst date, record the outcome. Framework right or wrong. Analyst right or wrong. Update the scorecard. Publish misses at the same prominence as hits.

### What "right" means

A prediction is confirmed when:
- **Recurrence**: the same failure class occurs again (same CRL reason, same endpoint miss, same safety signal)
- **Cascade**: multiple pipeline candidates fail on the same mechanism within the predicted timeframe
- **Fix**: the company implements the predicted fix and outcomes improve (harder to score — requires longer follow-up)
- **Death**: the company ceases meaningful R&D activity (runs out of cash, gets acquired for parts, pivots entirely)
- **Mitosis**: the platform/infrastructure becomes a separate business unit, spin-off, or is licensed independently

A prediction is refuted when the opposite occurs within the stated timeframe, or when the stated timeframe expires without the predicted event.

### What we're not predicting

- Whether the drug works (biology). That's the analyst's domain.
- Stock price. Price is downstream of many factors beyond the learning loop.
- Timing of regulatory decisions. FDA has its own pipe.

We're predicting whether the company's consolidate stack will produce a meaningfully different outcome next time. Process, not product.

## 2026-03-20: Tooling setup

### Target selection
Decided to go head-to-head with Martin Shkreli's public biotech positions from 2025-2026. He's a named analyst with timestamped, falsifiable calls — perfect for the scorecard.

**Shkreli's positions (seeded into DB):**
- CAPR (Capricor Therapeutics) — shorted, 46-page report, said HOPE-3 "will not work". Stock +440%. Admitted "bad call". → Run 0 retrospective.
- SPRB (Spruce Biosciences) — long, targets $500, BLA submission Q4 2026. → Run 1 forward.
- QURE (uniQure) — was long AMT-130, sold Nov 2025.
- ATYR (aTyr Pharma) — short, predicted 80% crash.
- INMB (Inmune Bio) — predicted 90% drop.

### Scripts and database
- `schema.sql` — relational schema: company, pipe (recursive tree), trauma, prediction, analyst_call, scorecard view. Embedding tables for pipe descriptions and trauma descriptions.
- `init_db.py` — creates DB, seeds 5 companies and 2 CAPR traumas.
- `embed.py` — embeds pipe/trauma descriptions using all-MiniLM-L6-v2. Includes `find_similar_traumas()` for recurrence probes via cosine similarity.
- `diagnose.py` — CLI for building pipe trees (`add_pipe`, `diagnose_pipe`), recording predictions (`add_prediction`), analyst calls (`add_analyst_call`), scoring (`score_prediction`), and displaying results (`tree TICKER`, `scorecard`).
- `prereg.md` — pre-registration for the biotech pilot.

All verified working. DB initialized with 5 companies, 2 traumas embedded, scorecard empty and waiting.

### Next
- Build the CAPR pipe tree (retrospective): map Capricor's org to the consolidate stack, trace HOPE-2 → HOPE-3 iteration, diagnose whether the framework would have predicted the positive result.
- Research HOPE-2 vs HOPE-3 differences on ClinicalTrials.gov to check the consolidate heuristic.
