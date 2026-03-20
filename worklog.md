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

### Research protocol: semiblind-semiblind merge

The diagnosis research itself uses the framework's Attend step — diverse selection with redundancy control.

**Architecture**: 2×2 Claude subagents for search, 2 codex instances for merge.

**Search layer (4 Claude subagents, run in parallel):**

| Instance | Search angle | Primary data source |
|---|---|---|
| Cache-A | Forward pass probes: is the molecule's pipeline broken? | ClinicalTrials.gov, PubMed |
| Cache-B | Forward pass probes: same angle, independent search | SEC EDGAR, financial media |
| Consolidate-A | Backward pass probes: is the company learning? | FDA letters, trial amendments |
| Consolidate-B | Backward pass probes: same angle, independent search | Conference presentations, analyst reports |

- **Semi-blind**: all agents share the framework vocabulary (six roles, two stacks, probe language) but don't see each other's findings during search.
- **Stochastic**: agents start from different data sources so they don't converge on the same evidence. The diversity is in the entry point, not the lens.
- **2 instances per angle**: if both Cache agents find the same evidence independently, it's high-confidence signal. If they diverge, the divergence itself is diagnostic.

**Attend (top-2 selection):**
- From the 4 agent outputs, select the top 2 based on evidence quality, novelty, and internal consistency.
- The other 2 are discarded — they served as diversity insurance during search. If they found nothing the top 2 missed, the search was thorough enough.

**Merge layer (2 codex instances, independent):**

| Instance | Input | Job |
|---|---|---|
| Codex-A | Top 2 agent outputs | Merge into single SOAP note with refs |
| Codex-B | Top 2 agent outputs | Same job, independent. Doesn't see Codex-A's output |

**SOAP note format:**
- **S** (Subjective): What the company/analysts say about themselves. Narrative from SEC filings, press releases, analyst reports.
- **O** (Objective): Hard data. Trial results, FDA letters, ClinicalTrials.gov entries, financial metrics.
- **A** (Assessment): Framework diagnosis. Which stack, which stage, which prediction type. How the evidence maps to the pipe tree.
- **P** (Plan): The falsifiable prediction. Claim, catalyst date, timeframe, analyst position for head-to-head.
- **Refs**: Links to all public sources cited.

- **Semi-blind merge**: both codex instances see the same top-2 evidence but judge independently. Agreement = high confidence. Disagreement = needs human judgment.

**Human Attend**: the user reads both SOAP notes, picks or synthesizes into the final published diagnosis. Skills automate Filter, human keeps Attend.

## 2026-03-20: Prereg tightening (codex sniff test #2)

Codex reviewed the actual prereg.md. Verdict: "Solid as a pilot operations plan. Weak as a true pre-registration." Key issues and how we addressed them:

1. **Prediction template must force binary resolution.** Added: every prediction must be PASS/FAIL on a specific catalyst within a specific window. If it can't be expressed this way, it's not ready to publish.

2. **"Analyst consensus" was undefined.** Replaced with: mechanical extraction of Shkreli's most recent public stance, mapped to bull/bear/neutral using fixed rules. One framework prediction vs. one analyst call. No consensus aggregation.

3. **Void bucket was dangerous.** Tightened: void only if catalyst is cancelled entirely. Delays are scored — window extends by one quarter, max one extension. Delays themselves are evidence for process predictions.

4. **Human merge was a leakage point.** Fixed: when codex instances disagree, human selects one (not synthesizes). Both are published. Selection committed before catalyst date.

5. **Run 0 was implicitly supporting accuracy claims.** Relabeled: "demonstration only." Does not count toward accuracy.

6. **Needed baselines beyond Shkreli.** Added: naive base rate (historical Phase 3 success rates from BIO/Informa) and always-pessimistic baseline. Primary endpoint for Run 1: beat pessimism.

7. **Target list was seeds, not frozen.** Frozen: Run 0 = CAPR, QURE. Run 1 = SPRB, ATYR, INMB. No additions or removals.

8. **Mixed outcomes unaddressed.** Added: prediction template requires specifying which endpoint determines resolution. Scored against that endpoint only.

9. **One prediction per catalyst rule.** Added: no stacking multiple predictions on the same company.

10. **Negativity bias.** Added as known bias #8, controlled by specificity requirement and always-pessimistic baseline.

11. **Downgraded success criterion.** Run 1 primary endpoint: framework accuracy > always-pessimistic baseline. At N=3, this means at least one correct PASS prediction.

12. **No special exemptions for biology.** If the drug fails for biological reasons, prediction still resolves as PASS or FAIL on the stated catalyst.

## 2026-03-20: Prereg tightening (codex sniff test #3)

Four final fixes:

1. **Merge tiebreak**: `soap-a` wins by default. No human selection.
2. **Dropped forced PASS**: if all predictions are FAIL, run is non-discriminating vs. pessimism. That's a result.
3. **Freeze point**: explicit commit after Run 0, before Run 1. Message: "Freeze: Run 0 complete, Run 1 locked."
4. **Per-company catalyst appendix**: locked exact catalyst, source, window, and PASS/FAIL conditions for all three Run 1 companies:
   - **SPRB**: BLA submission for TA-ERT, by 2026-12-31. PASS = submitted and accepted.
   - **ATYR**: FDA Type C meeting outcome for efzofitimod, by 2026-06-30. PASS = viable regulatory path confirmed. Note: Phase 3 already missed primary endpoint — this is about whether the company's consolidate stack can find a path from failure.
   - **INMB**: MAA submission to UK MHRA for CORDStrom, by 2026-09-30. PASS = submitted and acknowledged.

Also added explicit scope section and statistical posture (descriptive only, no inferential claims at N=3).

## 2026-03-20: CAPR search dispatched + temporal network insight

### CAPR search (4 agents dispatched)
Launched 4 parallel agents on CAPR per protocol. Cache-B returned first with excellent data from SEC EDGAR filings.

Cache-B key finding: the forward pass was **broken and rebuilt**, not patched. The original BLA (2024) tried to skip from HOPE-2 (n=20, Phase 2, cardiac subscore, natural history comparison) directly to approval. FDA rejected at Attend→Remember handoff (CRL: "did not meet substantial evidence of effectiveness"). Company then ran HOPE-3 (n=106, Phase 3, placebo-controlled, full PUL v2.0 primary + LVEF key secondary). Resubmission accepted, PDUFA August 22, 2026.

### Temporal network reframe (INVALIDATES static tree)

User's insight from Prof. Joseph Peters (SFU): our pipe tree is a temporal network, not a static tree. Peters' sequence-based dynamic graphs (Theory of Computing Systems, 2019) model exactly this — same node set, different edge states per time snapshot, with composition and test operations.

**What this changes:**
- The pipe tree topology (nodes = handoffs, roles) is stable across time
- The *states* (functional/broken/stressed/repaired) vary per snapshot
- The consolidate heuristic is a temporal connectivity test: does information propagate from failure at t₁ to repair at t₂?
- Schema updated: added `snapshot` and `pipe_state` tables, removed status/diagnosis from `pipe`

**CAPR as temporal graph (from Cache-B data):**

| Handoff | t₁ (HOPE-2/BLA era) | t₂ (HOPE-3 era) |
|---|---|---|
| Perceive → Cache | Functional | Stressed (two-facility split, CMC issues) |
| Cache → Filter | Functional | Functional (widened slightly) |
| Filter → Attend | Broken (subscore endpoint, n=20) | Repaired (PUL v2.0 total, n=106) |
| Attend → Remember | Broken (CRL, insufficient evidence) | Functional (PDUFA Aug 2026) |

Two handoffs were broken at t₁ and repaired at t₂. That's temporal connectivity — the consolidate stack propagated the failure signal backward and the forward pass was rebuilt. Framework would have predicted PASS on HOPE-3 because the consolidate stack was functional.

**Shkreli's error through this lens:** his 46-page short report analyzed the forward pass at t₁ ("the drug won't work") without checking whether the consolidate stack had repaired the broken handoffs by t₂. He diagnosed a snapshot, not a trajectory.

### CAPR search invalidated
The 4 agents were dispatched with the old static-tree framing. Their data is still useful as raw evidence, but the search reports need to be restructured as temporal sequences (pipe states across snapshots), not static handoff assessments. Will reformat when all agents return.

### All 4 agents returned

**Top 2 selected for merge (per protocol):**

1. **Consolidate-A** (strongest): Four-snapshot temporal sequence (ALLSTAR→HOPE-1→HOPE-2→HOPE-3). Found the full iteration history — indication pivot (MI→DMD), route change (intracoronary→IV), dose escalation (25M→150M), endpoint evolution (scar size→PUL 1.2→PUL v2.0+LVEF). Trauma recurrence: ALLSTAR failure class (wrong indication/route) did not recur. CRL is a different failure class (regulatory packaging). All three consolidate stages assessed as functional.

2. **Cache-B** (second): SEC filings perspective. CRL details, two-facility manufacturing risk, endpoint strategy evolution, $150M raise. Assessed Filter→Attend as "repaired after failure" — the key finding. Original BLA tried to skip from n=20 Phase 2 to approval; FDA rejected; HOPE-3 was the structural fix.

**Notable from other two agents (kept as audit trail):**
- Cache-A: biodistribution gap (no published evidence CDC exosomes reach skeletal muscle), p-value attenuated from HOPE-2 (0.014) to HOPE-3 (0.029) despite 5x patients
- Consolidate-B: READ stage impaired (management spin on HOPE-2 results), securities fraud class action, Shkreli's critique was primarily forward pass ("drug won't work") not backward pass

**Codex merge dispatched**: 2 independent instances merging top 2 into recursive SOAP notes with temporal snapshots.

### Codex SOAP merge complete

Both instances agree. Diagnosis: consolidate stack was functional and compounding across four snapshots. Shkreli diagnosed the forward pass at one snapshot; the framework diagnoses the backward pass trajectory. No merge disagreement — both produced the same assessment independently.

Key line from SOAP-B: "the framework would have been long the trajectory, not necessarily long the t₃ snapshot."

### CAPR Run 0 demonstration: complete

The framework would have predicted PASS on HOPE-3 because:
1. ALLSTAR failure was absorbed, not repeated (no trauma recurrence)
2. Each trial structurally rewrote the weak interfaces (indication, route, dose, endpoints, sample size)
3. The CRL was a different failure class (regulatory packaging, not mechanism)
4. The consolidate stack was functional at all three stages

This is structurally distinct from Shkreli's analysis, which was a forward-pass snapshot critique ("the drug won't work"). The framework adds the temporal dimension he missed.

### Next
- Rebuild init_db.py and diagnose.py for temporal schema
- Commit all CAPR artifacts
- Freeze protocol for Run 1
