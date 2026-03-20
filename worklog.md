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

### Files created
- `README.md` — project overview
- `CLAUDE.md` — agent context
- `taxonomy.md` — recursive tree structure
- `probes.md` — diagnostic probes by stack and fault site
- `design.md` — full design doc with goal, prediction types, runs, coordination
- `biotech.md` — biotech pilot: org-chart mapping, prediction examples, data sources
- `worklog.md` — this file
