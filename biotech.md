# Biotech Pilot

## The framing

The molecule is the pipe. The company is its consolidate stack.

The molecule's forward pass is chemistry: compound → binding → effect → outcome. The company exists to run the backward pass: read outcomes (clinical data), batch process them (interpret, iterate), write back to the substrate (modify the compound). The entire company is the molecule's learning loop.

## Mapping the org chart to Consolidate

| Consolidate stage | Function | Teams |
|---|---|---|
| **Read outcomes** | Collect and clean trial results | Clinical ops, data management, biostatistics |
| **Batch process** | Interpret results, decide what to change | R&D, medicinal chemistry, computational biology |
| **Write substrate** | Modify the compound, get it back into the world | Manufacturing, formulation, regulatory |

## The molecule's forward pass (cache stack)

| Handoff | What happens | Failure mode |
|---|---|---|
| **Perceive → Cache** | Compound enters biological system, binds to target | Wrong target, poor bioavailability — the molecule isn't being "read" by the body |
| **Cache → Filter** | Binding produces downstream effects, some therapeutic, some toxic | No selectivity — side effects aren't filtered from intended effects |
| **Filter → Attend** | Among viable effects, the therapeutic window is selected | Window too narrow, dose-response curve isn't navigable |
| **Attend → Remember** | Therapeutic effect persists in the patient | Effect doesn't last, drug is cleared too fast, resistance develops |

## Prediction types applied to biotech

### Type 1: Recurrence
The company reads outcomes but doesn't change the compound meaningfully between trials. Same mechanism, same indication, same failure.

**Diagnostic probe**: Compare the compound modification between Trial N and Trial N+1 after a failure. If the changes are cosmetic (dose adjustment, endpoint redefinition, patient selection tweaks) rather than structural (new mechanism, new target, new scaffold), the batch process stage is broken.

**What to look for in public data**:
- ClinicalTrials.gov: compare intervention descriptions across sequential trials
- FDA complete response letters: do they cite the same deficiency twice?
- SEC filings: does the pipeline narrative change after a failure, or does it just add caveats?

### Type 2: Cascade
Broken Filter → Attend handoff: the company advances too many similar candidates without diversity.

**Diagnostic probe**: Count the number of pipeline candidates sharing the same mechanism of action. High count with low structural diversity = broken Attend. If one fails, the rest are correlated — they'll fail for the same reason.

**What to look for**:
- Pipeline disclosures in 10-K filings
- Conference presentations showing "platform" candidates that are minor variations
- Competitors' failures on the same target (the entire sector can have a broken Attend)

### Type 3: Fix
Diagnose the missing algorithm → predict which parts bin entry fixes it.

**Examples**:
- Broken Attend (no diversity): add DPP-style candidate selection across mechanisms, not just targets
- Broken Filter (over-filtering): predictive biomarkers to rescue compounds that failed in broad populations but work in subgroups
- Broken Read (wrong outcomes): switch from surrogate endpoints to real clinical outcomes

### Type 4: Death
Multiple broken roles, the loop cannot self-correct.

**Pattern**: Company can't write back to substrate. Manufacturing fails (can't produce at scale), regulatory blocks (can't get approval to re-enter patients), or funding runs out (can't finance another iteration). The backward pass is severed. The molecule stops iterating.

**What to look for**:
- Cash runway vs. time to next data readout
- CMC (chemistry, manufacturing, controls) deficiencies in FDA letters
- Multiple clinical holds

### Type 5: Mitosis
The company's Read stage (data platform, clinical ops infrastructure) outgrows the therapeutic pipeline it serves.

**Diagnostic probe**: What fraction of headcount or budget goes to the platform vs. the therapeutic programs? When the platform is serving external customers or being licensed out, mitosis is imminent.

**What to look for**:
- CRO partnerships that evolve into spin-offs
- "Platform" companies that start partnering their technology separately from their pipeline
- Internal tools becoming products (screening platforms, AI drug discovery engines)

**Retrospective examples**:
- Companies that started as drug developers and became platform/tools companies
- Pharma companies that spun off their clinical data operations

## Acquisition as consolidate-stack purchase

A pharma giant acquiring a biotech is buying a consolidate stack. The acquirer's own backward pass is too slow for a novel mechanism — its Read/Process/Write cycle takes decades. The biotech has already iterated the molecule through several cycles. The acquisition imports a faster consolidate stack.

**Prediction**: Acquisitions where the acquirer already has a working consolidate stack for the same mechanism class will underperform. The acquired company's consolidate stack is redundant — the acquirer is paying for iterations it could have done itself. Acquisitions where the mechanism is genuinely novel to the acquirer should outperform.

## Head-to-head with analysts

Biotech analysts are mini-celebrities with public track records. The legitimacy play: make timestamped predictions that directly contradict named analysts, then score both.

**The edge**: Analysts have domain depth (biology, regulatory, management) but no structural theory of the learning loop. They predict whether the drug works. The framework predicts whether the *company can iterate* — will the next compound be meaningfully different, or will they repeat the same failure? Process prediction vs. outcome prediction.

**Format**: For each prediction, record:
- The framework's prediction and reasoning (which stack, which stage, which prediction type)
- The analyst consensus or a specific named analyst's call
- The outcome
- Who was right

**Scorecard honesty**: Publish misses with the same prominence as hits. Analysts rarely publish their miss rate. A public loss record is itself a credibility signal.

**Distribution**: The analyst community is small. One correct non-obvious call that contradicts a known analyst gets noticed. The prediction doesn't need to be right every time — it needs to be right on cases the analysts got wrong.

## Data sources

All free or cheap:
- **ClinicalTrials.gov** — trial designs, endpoints, results, amendments
- **FDA databases** — approval letters, complete response letters, clinical holds
- **SEC EDGAR** — 10-K pipeline disclosures, risk factors, MD&A
- **PubMed** — published trial results, mechanism papers
- **Stock price** — timestamps confirmation/refutation of predictions

## First candidates for Run 0

Criteria for retrospective case selection:
1. At least two trials on the same target/mechanism with public results
2. Clear outcome (approval, failure, pivot, spin-off, acquisition, death)
3. Enough public documentation to run the diagnostic tree 2-3 levels deep

**Catalyst calendar**: Biotech has pre-scheduled events — quarterly earnings, PDUFA dates, trial readouts, conference presentations (ASCO, AACR, JPM). Publish predictions before a known catalyst date. Outcome is public within days. No ambiguity about timing.

This gives the fastest possible iteration cycle for the scorecard. One prediction can be tested per quarter, not per decade.

TODO: Select 3-5 specific companies.
