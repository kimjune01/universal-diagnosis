# Pre-registration: Biotech Pilot

**Status**: Protocol-feasibility pilot. Not evidence that the framework works scientifically. The goal is one credible proof of concept.

## Research question

Can the Natural Framework's recursive pipe diagnosis generate binary predictions about biotech catalyst outcomes that match or exceed a named analyst's accuracy on the same catalysts?

## Design

- **Run 0** (demonstration only): 3-5 companies with known outcomes. Diagnose post hoc. Does the framework explain the outcome in a way that adds to the analyst narrative? Run 0 does not support accuracy claims — it calibrates the process.
- **Run 1** (prospective): 3-5 companies with upcoming catalyst dates. Diagnose, predict, publish before the date. Score against analyst. This is the only run that counts for accuracy.

## Target list

Targets are drawn from Martin Shkreli's public biotech positions (2025-2026). Shkreli is chosen because:
- Named, public, timestamped calls with clear bull/bear positions
- High-profile enough that head-to-head comparison is attention-worthy
- Has a documented miss (CAPR) and active forward positions (SPRB, ATYR, INMB)

### Frozen target list

The final list is locked before any diagnosis begins. No additions or removals after this point. All companies on the list are diagnosed — no cherry-picking.

**Run 0 (demonstration):** CAPR, QURE
**Run 1 (prospective):** SPRB, ATYR, INMB

If a company fails inclusion criteria during diagnosis (e.g., insufficient trial history for recurrence probes), it is marked as excluded with reason, not replaced.

## Inclusion criteria

- Public biotech company (SEC filings available)
- At least two trials or FDA interactions on the same program (enough history for recurrence probes)
- Upcoming catalyst within 6 months (Run 1 only)
- Named analyst coverage exists for head-to-head comparison

## Scope

This pilot tests one thing: whether the Natural Framework's diagnosis of a biotech company's learning loop (consolidate stack) produces useful predictions about upcoming catalysts. It is champion vs. challenger — Shkreli is the champion, the framework is the challenger, same companies, same catalysts, same scorecard.

What is in scope:
- Binary PASS/FAIL predictions on specific biotech catalysts
- Head-to-head comparison with one named analyst on the same catalysts
- Descriptive accuracy reporting at N=3 (no inferential claims)

What is out of scope:
- Validating the Natural Framework as a universal theory
- Predicting drug efficacy (biology)
- Predicting stock price
- Predicting FDA timing
- Generalizing beyond biotech
- Generalizing beyond Shkreli's picks

### Freeze point
All prompts, heuristics, inclusion criteria, merge rules, and scoring rules are frozen after Run 0 completes and before any Run 1 diagnosis begins. The freeze is marked by a single commit with the message "Freeze: Run 0 complete, Run 1 locked." No changes to the protocol after that commit.

## Methods

### Diagnosis process
1. Identify the molecule-as-pipe: compound, target, mechanism, indication
2. Map the company to the consolidate stack: who reads outcomes (clinical ops), who processes them (R&D), who writes back to substrate (manufacturing, regulatory)
3. Run the stack-level probe: is the forward pass broken (wrong output now), or is the backward pass broken (hasn't improved over time)?
4. Check for trauma recurrence: find known failures, check if the same class recurred
5. Classify prediction type: recurrence, cascade, fix, death, or mitosis
6. Record analyst position for head-to-head

### Research protocol: semiblind-semiblind merge
Each company diagnosis is conducted by 4 Claude subagents searching in parallel, then merged by 2 codex (GPT-5.4) instances independently.

**Search layer** (4 agents, parallel, semi-blind — share framework vocabulary, don't see each other's findings):
- Cache-A: forward pass probes via ClinicalTrials.gov, PubMed
- Cache-B: forward pass probes via SEC EDGAR, financial media
- Consolidate-A: backward pass probes via FDA letters, trial amendments
- Consolidate-B: backward pass probes via conference presentations, analyst reports

**Attend**: select top 2 of 4 agent outputs based on evidence quality, novelty, and internal consistency. The other 2 served as diversity insurance.

**Merge layer** (2 codex instances, independent — see top-2 outputs, don't see each other's merge):
- Each merges the top 2 into a single SOAP note with refs:
  - **S** (Subjective): company/analyst narrative (SEC filings, press releases, analyst reports)
  - **O** (Objective): hard data (trial results, FDA letters, ClinicalTrials.gov, financials)
  - **A** (Assessment): framework diagnosis (which stack, which stage, which prediction type)
  - **P** (Plan): falsifiable prediction using the prediction template below
  - **Refs**: links to all public sources cited

**Merge disagreement rule**: If the two codex SOAP notes produce different primary predictions, `soap-a` is the primary by default. `soap-b` is recorded as the alternate. No human selection, no synthesis. Both are published. If the merges agree, that prediction is the primary.

The 2×2 redundancy serves as the diversity guarantee. If both instances of a search angle find the same evidence independently, it's signal. Divergence is also signal.

### Tools
- SQLite database with relational schema (companies, recursive pipe tree, traumas, predictions, analyst calls)
- Sentence embeddings (all-MiniLM-L6-v2) for semantic matching of trauma descriptions and pipe descriptions
- Cosine similarity threshold (0.6) for recurrence probe: "is this failure similar to a prior failure?"
- Public data sources: ClinicalTrials.gov, FDA databases, SEC EDGAR, PubMed

### Operational settings
- **Search subagents**: Claude Opus 4.6 (claude-opus-4-6), 4 instances per company
- **Merge**: Codex CLI with GPT-5.4, 2 instances per company
- **Embeddings**: all-MiniLM-L6-v2 via sentence-transformers
- **Cosine similarity threshold**: 0.6 for trauma recurrence matching
- **Temperature**: default for all models (not overridden)
- **Prompts**: committed to repo before first diagnosis, not modified between companies

### The consolidate heuristic
The cheap probe for diagnosing the backward pass: instead of "is this company learning?" (expensive), ask "has this company repeated a known failure?" (cheap event matching). `count(similar_failures) > 1` = broken consolidate. Similarity is measured via embedding cosine similarity on failure descriptions.

## Prediction template

Every primary prediction must be forced into this binary format before publication:

```
Company: [TICKER]
Catalyst: [exact event, e.g., "HOPE-3 Phase 3 topline readout"]
Source: [exact source that determines outcome, e.g., "ClinicalTrials.gov results posting" or "FDA PDUFA action letter"]
Window: [exact date range, e.g., "Q4 2026" or "by 2026-12-31"]
Prediction: [PASS or FAIL]
Reasoning: [one sentence — which stack, which stage, which prediction type]
Analyst position: [bull/bear/neutral, name, date, source URL]
```

If the prediction cannot be expressed as PASS/FAIL on a specific catalyst within a specific window, it is not ready to publish.

## Analyst benchmark rule

For each company, the analyst position is extracted mechanically:

1. Find Shkreli's most recent public statement about the company before the catalyst date
2. Map to bull/bear/neutral:
   - **Bull**: long position, price target above current, or explicit "will work/approve" statement
   - **Bear**: short position, price target below current, or explicit "will fail/not work" statement
   - **Neutral**: no position or explicitly undecided
3. Record the source URL and date

This is the only comparator. No consensus aggregation across multiple analysts — one framework prediction vs. one analyst call, same catalyst, same window.

### Additional baselines

For context (not primary endpoint):
- **Naive base rate**: historical success rate for similar biotech catalysts (e.g., Phase 3 oncology trials have ~50% success rate; gene therapy BLAs have ~X%). Sourced from BIO/Informa clinical development success rates reports.
- **Always-pessimistic baseline**: predict FAIL on every catalyst. If the framework can't beat pessimism, it's not adding signal.

## Artifacts produced per company

Each company diagnosis produces the following artifacts, committed to the repo:

1. **4 search reports** (`searches/{TICKER}/cache-a.md`, `cache-b.md`, `consolidate-a.md`, `consolidate-b.md`) — raw agent outputs with stack traces. Each report traces the path through the pipe tree: which node was expanded, which stack was probed, what evidence was found, what was ruled out, and which child was expanded next. The stack trace is the audit trail — it shows why the agent went deeper at one node and not another. Kept even after top-2 selection.
2. **2 SOAP notes** (`notes/{TICKER}/soap-a.md`, `soap-b.md`) — codex merge outputs. Independent diagnoses in SOAP format with refs. These are recursive: each pipe node in the tree gets its own nested SOAP entry (stack-level probe, then each child pipe). Expect these to be long — a company decomposed 3 levels deep will have dozens of nested entries.
3. **1 final diagnosis** (`diagnoses/{TICKER}.md`) — determined by merge agreement or `soap-a` default. This is the published prediction in the template format above.
4. **Pipe tree in DB** — the recursive decomposition of the company, queryable via `diagnose.py tree TICKER`.
5. **Prediction record in DB** — the falsifiable claim, catalyst date, analyst position, outcome (pending until scored).
6. **Trauma records in DB** — known failures with embeddings, used for recurrence probes on this and future companies.

### Artifact lifecycle
- Search reports and SOAP notes are write-once. Never edited after creation.
- The final diagnosis is write-once after publication. Never revised.
- Prediction outcomes are updated exactly once, after the catalyst date.
- The scorecard is a live view, regenerated from the DB on each query.

## Predictions per company

Each diagnosis produces exactly one primary prediction in the template format above. Secondary predictions allowed but scored separately and do not count toward the primary endpoint.

### Specificity note
If all Run 1 primary predictions are FAIL, the run is deemed non-discriminating versus the always-pessimistic baseline. This is itself a result — it means the framework cannot distinguish healthy systems from broken ones on this sample. No predictions are forced to PASS.

## Scoring

The judge is ground truth, not a model. No LLM scores predictions. Outcomes are determined exclusively by:
- **Trial results**: published endpoints from ClinicalTrials.gov or peer-reviewed journals
- **FDA actions**: approval letters, complete response letters, clinical holds, breakthrough designations
- **Corporate actions**: spin-offs, acquisitions, pipeline changes filed with the SEC
- **Market events**: stock price movement on catalyst dates (timestamps confirmation, not the prediction itself)

These are public, timestamped, and not subject to interpretation. If the outcome requires judgment to score, the prediction was poorly specified.

### Resolution rules
- **Hit**: predicted event occurs within stated window, confirmed by the pre-specified source
- **Miss**: predicted event does not occur within stated window, or opposite occurs
- **Void**: ONLY if the catalyst is cancelled entirely (not delayed). Delays are scored as follows:
  - If the prediction was FAIL and the catalyst is delayed: scored as pending, window extends by one quarter, max one extension
  - If the prediction was PASS and the catalyst is delayed: scored as pending, same extension rule
  - If the prediction was about process (recurrence, death, mitosis) and the company delays: the delay itself is evidence and must be evaluated against the prediction

### Mixed outcomes
If a trial readout is mixed (e.g., hits secondary endpoint but misses primary), the prediction is scored against the pre-specified source and endpoint. The prediction template requires specifying which endpoint determines resolution.

### One prediction per catalyst
Each company gets one primary prediction on one catalyst. No stacking multiple predictions on the same company to increase chances.

## Commitment

- Publish all predictions before catalyst dates
- Publish all outcomes regardless of result
- Do not revise predictions after publication
- Report hit rate, miss rate, and void rate separately
- Compare framework hit rate to Shkreli's hit rate on the same catalysts
- Compare framework hit rate to naive base rate and always-pessimistic baseline

## Success criterion

Run 0 (demonstration): The framework produces at least one explanation that is structurally distinct from the analyst narrative. This is qualitative and does not support accuracy claims.

Run 1 (prospective, primary endpoint): Framework and Shkreli accuracy on the same 3 locked catalysts, reported side by side. No inferential claim at N=3 — results are descriptive only. Secondary check: framework accuracy vs. always-pessimistic baseline. If all predictions are FAIL, the run is non-discriminating vs. pessimism.

## Known biases

1. **Selection bias**: Targets are chosen from one analyst's positions, not randomly sampled. Shkreli's picks skew toward controversial, high-volatility names. Mitigated by freezing the target list and diagnosing all companies on it.

2. **Confirmation bias**: The diagnostician (us) created the framework and wants it to succeed. Mitigated by:
   - Binary prediction template (no wiggle room in scoring)
   - Publishing before catalyst date
   - Mechanical heuristic (embedding similarity) where possible
   - Publishing misses at same prominence as hits

3. **Hindsight bias** (Run 0 only): Retrospective diagnoses benefit from knowing the outcome. Run 0 is labeled demonstration only and does not support accuracy claims.

4. **Domain naivety**: We are not biotech domain experts. Mitigated by using only public, verifiable data sources and documenting the mapping explicitly.

5. **Small N**: 3 companies in Run 1 is not statistically powered. A lucky streak is indistinguishable from a working framework. This is a pilot.

6. **Survivorship bias in trauma data**: Recurrence probe only works on documented failures.

7. **Embedding model limitations**: all-MiniLM-L6-v2 may not capture biotech-specific semantic similarity. Fallback: manual category labels.

8. **Negativity bias**: The framework may systematically diagnose "broken" more often than "functional" because the probes are designed to find faults. The always-pessimistic baseline and specificity requirement partially control for this.

## Appendix: Run 1 catalyst definitions

### SPRB (Spruce Biosciences)
- **Catalyst**: BLA submission for TA-ERT (tralesinidase alfa) for Sanfilippo Syndrome Type B (MPS IIIB)
- **Source**: Spruce Biosciences press release via investors.sprucebio.com or SEC 8-K filing
- **Window**: by 2026-12-31 (company guidance: Q4 2026)
- **PASS condition**: BLA submitted to FDA and acknowledged (filing accepted)
- **FAIL condition**: BLA not submitted by end of window, or submission withdrawn/rejected
- **Shkreli position**: Bull (long, targets $500, "will be approved")

### ATYR (aTyr Pharma)
- **Catalyst**: FDA Type C meeting outcome for efzofitimod in pulmonary sarcoidosis (EFZO-FIT Phase 3 missed primary endpoint; meeting determines regulatory path forward)
- **Source**: aTyr Pharma press release via investors.atyrpharma.com or SEC 8-K filing
- **Window**: by 2026-06-30 (company guidance: mid-April 2026 meeting, results disclosed shortly after)
- **PASS condition**: FDA confirms a viable regulatory path forward (e.g., agrees to accept secondary endpoints, allows supplemental filing, or requests additional trial with defined path)
- **FAIL condition**: FDA does not provide a viable path forward (e.g., requires full new Phase 3 with no agreed endpoint)
- **Shkreli position**: Bear (short, predicted 80% crash)

### INMB (Inmune Bio)
- **Catalyst**: MAA submission to UK MHRA for CORDStrom in recessive dystrophic epidermolysis bullosa (RDEB)
- **Source**: INmune Bio press release via inmunebio.com or SEC 8-K filing
- **Window**: by 2026-09-30 (company guidance: mid-summer 2026)
- **PASS condition**: MAA submitted and acknowledged by MHRA
- **FAIL condition**: MAA not submitted by end of window, or submission withdrawn/rejected
- **Shkreli position**: Bear (predicted 90% drop)

## Limitations

- Small N. This is a pilot, not a powered study.
- Selection bias in company choice. Mitigated by frozen target list.
- The diagnostician is not blind to analyst consensus. Mitigated by publishing framework diagnosis before looking up analyst positions where possible.
- We are predicting process (will the company iterate effectively?), not product (will the drug work?). If the drug fails for biological reasons unrelated to the learning loop, the prediction must still resolve as PASS or FAIL on the stated catalyst — no special exemptions.
- **Cash as escape hatch**: A broken consolidate stack does not mean immediate death. Cash runway is the timer. Death predictions must specify cash runway as the upper bound on survival time.
