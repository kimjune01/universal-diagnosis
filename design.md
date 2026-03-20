# Universal Diagnosis: Design

## Goal

Generate falsifiable predictions from the Natural Framework and publish them. The framework gets legitimized the way Mendeleev's table did: not by organizing what's known, but by predicting what isn't yet observed. The diagnosis tool is the prediction engine.

## How it works

1. **Diagnose** a system — walk the recursive tree, find the broken role
2. **Predict** the consequence — the handshake formalism says what breaks downstream when a contract is violated
3. **Predict** the fix — the parts bin says which algorithm fills the broken cell
4. **Publish** before the outcome — timestamp the prediction
5. **Verify** — reality confirms or refutes

Retrospective predictions work too: diagnose a system where the outcome is already known but the framework's explanation is novel. "The framework predicts Boeing's quality failures would recur because their Consolidate stack is broken at the outcome collection stage. Here's the 2018 evidence. Here's the 2024 recurrence."

## The tree

Every node is a pipe with the same shape:

```
Pipe
├── Cache stack (forward pass — is it broken right now?)
│   ├── Perceive → Cache
│   ├── Cache → Filter
│   ├── Filter → Attend
│   └── Attend → Remember
└── Consolidate stack (backward pass — has it failed to learn?)
    ├── Read outcomes
    ├── Batch process
    └── Write substrate
```

Each child is itself a pipe with the same structure. No special treatment for scale — a company, a microservice, and a single function all look the same to the algorithm. Recurse until rock bottom (atomic operation, single API call, one person making one decision).

## The consolidate heuristic

Diagnosing "is this system learning?" sounds expensive. The cheap heuristic: **check for trauma recurrence**. Find a known failure, check if it happened again. `count(similar_failures) > 1` is the probe.

This works at every scale:
- Company: same data breach twice
- Software: same bug class ships again
- Person: same mistake repeated
- Function: same exception on same input class

Recurrence of a known fault at a child node is evidence that the consolidate stack of the parent is broken. The child failed, the parent should have learned, it didn't. Diagnosis flows upward.

This heuristic is especially useful for predictions because trauma recurrence is retrospectively verifiable from public records.

## Prediction types

### Type 1: Recurrence prediction
Diagnose a broken consolidate stack → predict the same class of failure will recur.
- Strongest prediction type. Binary outcome. Publicly verifiable.
- Example: "Company X had incident Y. Their consolidate stack shows no structural change. Predict recurrence within Z timeframe."

### Type 2: Downstream cascade prediction
Diagnose a broken handoff → predict which downstream roles will degrade.
- The handshake formalism specifies what each role's postcondition guarantees to the next. A broken postcondition has a specific downstream signature.
- Example: "System X has a broken Filter → Attend handoff. Predict: Attend will drown in redundant candidates, Remember will persist noise, Consolidate will amplify wrong winners."

### Type 3: Fix prediction
Diagnose a missing or broken role → predict which algorithm from the parts bin will fix it.
- The parts bin catalogs algorithms by role, with preconditions and postconditions. A broken role has a specific shape; the fix is the algorithm whose postcondition fills the gap.
- Example: "System X has no diversity guarantee in Attend. Predict: adding MMR re-ranking (not just top-k) will improve output quality."

### Type 4: Death prediction
Diagnose multiple broken roles → predict pipeline death via one of three death conditions (broken step, closed loop, decaying input).
- Strongest claims. Hardest to verify (long time horizon). Most impressive when correct.
- Example: "System X has broken Filter AND broken Consolidate. The loop cannot self-correct. Predict: decay without external intervention."

### Type 5: Mitosis prediction
Diagnose a stack whose resource consumption exceeds its parent pipe's capacity → predict the stack will split into an independent pipe.
- The recursive structure predicts this: a stack is made of pipes, and when a pipe outgrows its host, it must either become autonomous or starve the sibling stack. Two outcomes, no middle ground.
- The split stack becomes a full pipe with its own two stacks. The parent pipe's former stack is replaced by a Perceive → Remember interface to the new pipe (an API, a contract, a vendor relationship).
- A fat stack that *doesn't* split is a death condition — it starves the other stack, which degrades the parent pipe.
- Retrospective examples: AWS (Amazon's cache infra split into its own pipe), Slack (Tiny Speck's communication cache outgrew the game), cell division (organelle load exceeds membrane capacity).
- Forward prediction: diagnose companies with oversized internal tooling, data platforms, or ops teams. Predict: spin-out or core degradation.
- Example: "Company X's internal ML platform consumes 40% of engineering headcount. Predict: either it ships as a product within Y timeframe, or the product org's velocity degrades measurably."

## Coordination protocol

Multiple agents can explore the tree in parallel. The protocol is marketing-speak — natural language pipe descriptions that are human-readable and serve as node identifiers.

An agent claims a node by writing: "I'm looking at [pipe description], [stack], [site]."

Other agents read the tree and avoid claimed subtrees. Like lock acquisition, but the lock name is a sentence a human can read and understand.

Why marketing-speak:
- Already a shared language across scales (CEO and junior engineer both understand "our onboarding pipeline is leaking")
- No translation layer between agent coordination and human oversight
- Vocabulary scales with the domain — agents pick up local jargon as they descend
- Diagnostic logs are human-readable for free

## Data structure

```
Node {
  description: string          // marketing-speak name of this pipe
  stack: cache | consolidate   // which pass is under investigation
  site: string                 // which handoff or stage
  children: [Node]             // refs to subpipes (populated on expansion)
  status: unexplored | claimed | diagnosed | cleared
  agent: string | null         // who holds the lock
  traumas: [Event]             // known failures for recurrence probes
  diagnosis: string | null     // conclusion, if any
  prediction: Prediction | null // what the framework predicts happens next
}

Prediction {
  type: recurrence | cascade | fix | death
  claim: string               // the falsifiable statement
  evidence: [string]           // what supports the diagnosis
  timeframe: string | null     // when to check (for forward predictions)
  published: date              // timestamp for priority
  outcome: confirmed | refuted | pending
}
```

## MCTS mechanics

At any node:
1. **Select**: UCB1 over children. Prefer unexplored nodes, then nodes with high uncertainty.
2. **Expand**: Decompose the selected pipe into its two stacks and their children. This is where domain knowledge enters — the agent needs to know what subpipes exist.
3. **Rollout**: Run a cheap probe at the expanded node. Cache stack: send test input, check output. Consolidate stack: check for trauma recurrence.
4. **Backpropagate**: Update parent nodes with the result. A diagnosed fault in a child informs the parent's status.

**Termination**: Node is rock bottom (can't decompose further) and probe returns a definitive result.

**Rollout policy**: Prefer cheap probes first. Escalate only when cheap ones are ambiguous.

| Cost | Cache stack | Consolidate stack |
|------|-------------|-------------------|
| Free | Check logs, inspect config | Check if scheduler is running |
| Cheap | Send test input, query DB | Find a past failure, check if it recurred |
| Moderate | Synthetic workload, A/B test | Compare behavior across time windows |
| Expensive | Instrument code, load test | Full feedback loop audit |

Key asymmetry: cache probes are spatial (test one thing now), consolidate probes are temporal (compare across time). The trauma recurrence heuristic makes the temporal comparison cheap by reducing it to event matching.

## Publication strategy

Predictions need to be published in a format that's:
- **Timestamped** — priority matters for legitimacy
- **Falsifiable** — each prediction has a clear pass/fail condition
- **Portable** — readable by people who don't know the framework (marketing-speak helps here)
- **Accumulating** — a scorecard of confirmed/refuted predictions builds credibility over time

The blog is the natural publication venue. Each diagnosis post is a prediction. The scorecard is a running tally.

## Runs

The project expands in stages. Each run is cheaper than the next, validates the machinery before scaling, and produces publishable predictions.

### Run 0: Retrospective validation (biotech pilot)
- **Sector**: Biotech. Chosen because data is public (ClinicalTrials.gov, FDA filings, SEC disclosures), outcomes are documented, and the market prices predictions in real time.
- Pick 3-5 biotech companies where the outcome is already known — trial failures, platform spin-offs, repeated regulatory rejections.
- Diagnose each using the framework. Show the framework would have predicted the known outcome.
- Focus on:
  - **Recurrence**: companies that failed a Phase 3, didn't fix the consolidate stack, and failed again on the same mechanism or indication.
  - **Mitosis**: companies whose internal discovery platforms outgrew the therapeutic pipeline and spun off (or should have).
  - **Cascade**: companies with a broken Filter → Attend handoff — advancing too many similar candidates without diversity.
- Purpose: calibrate the diagnostic process on a sector where the data is rich and the pipeline metaphor is literal. No risk — outcomes are known.
- Publish as blog posts. These aren't predictions yet, they're evidence that the lens is useful.

### Run 1: Forward predictions (biotech)
- Same sector, forward-looking. Pick 3-5 biotech companies with visible symptoms but unknown outcomes.
- Run shallow diagnoses (2-3 levels deep). Focus on Type 1 (recurrence) and Type 5 (mitosis) — cheapest probes, clearest pass/fail.
- The market provides fast feedback: stock movement after trial results, FDA decisions, or spin-off announcements timestamps confirmation or refutation.
- Timestamp and publish each prediction.
- Purpose: test whether the framework generates non-obvious predictions. Score after 6-12 months.

### Run 2: Deeper predictions with more types
- Expand to Type 2 (cascade) and Type 3 (fix) predictions. These require deeper tree expansion and more domain knowledge.
- Increase depth — go 4-5 levels into systems where you have better access (your own projects, open-source codebases you can instrument).
- Start building the scorecard: confirmed / refuted / pending.
- Purpose: test the handshake formalism and parts bin, not just the tree structure.

### Run 3: Agent-assisted diagnosis
- Build the MCTS tooling so agents can expand and probe the tree semi-autonomously.
- Test multi-agent coordination protocol on a real system.
- Generate predictions at higher volume.
- Purpose: test whether the process scales beyond manual diagnosis.

### Run 4: Type 4 (death) predictions
- Only attempt after the scorecard has enough confirmed predictions to be credible.
- Death predictions are the strongest claims and the most likely to attract attention — but also the most likely to damage credibility if wrong.
- Purpose: the big swing. If these land, the framework is taken seriously.

Each run feeds the next. Run 0 calibrates the lens. Run 1 tests it. Run 2 deepens it. Run 3 scales it. Run 4 bets on it.

## Open questions

1. **Target selection**: Which systems to diagnose first? Criteria: publicly observable, enough history for trauma recurrence checks, interesting enough that correct predictions get attention. Public companies (already started with diagnosis-company). Open-source projects. Government agencies.

2. **Expansion knowledge**: When an agent decomposes a pipe, where does it get the list of subpipes? Options: (a) ask the system owner, (b) infer from documentation/code, (c) use the six roles as a template and ask "what does Perceive look like here?"

3. **Description deduplication**: Two agents might describe the same pipe differently. The marketing-speak protocol needs some normalization — embedding similarity on descriptions, or explicit aliases.

4. **Prediction timeframe**: Recurrence predictions need a window. Too short and you miss slow failures. Too long and the prediction is unfalsifiable. What's the right default?

5. **Scorecard honesty**: Must publish refuted predictions with the same prominence as confirmed ones. Cherry-picking kills credibility.
