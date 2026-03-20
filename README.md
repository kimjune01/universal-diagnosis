# Universal Diagnosis

Cheap Attend for agents: diagnose information systems using MCTS over a universal fault taxonomy derived from the Natural Framework.

## The idea

Blind-blind-merge works but is expensive — it runs multiple parallel solvers and merges results. Diagnosis is the cheap alternative: instead of exploring everything, eliminate branches fast.

Every information system has six roles (Perceive → Cache → Filter → Attend → Remember, with Consolidate as the backward pass). This gives a portable fault tree that works across domains without needing system-specific topology.

## MCTS as diagnostic search

- **Tree**: sector → domain → function → pipe stage (which of the six roles is broken?)
- **UCB1**: balance drilling into the most likely fault vs. checking adjacent components
- **Rollouts**: cheap probes — ask a diagnostic question, observe the response
- **Backpropagation**: update beliefs about which branch contains the fault

## Storage

Semantic database with controlled vocabulary:
1. **Taxonomy** — sector/domain/function labels (the tree MCTS navigates)
2. **Symptom → hypothesis mappings** — observations that narrow branches
3. **Probe catalog** — cheap questions you can ask at each node

## What's new

Traditional fault diagnosis assumes known system topology. The Natural Framework provides a *universal* topology — the six roles are the diagnostic tree structure, portable across domains.

## Open questions

- What's the right granularity for the taxonomy? Sector/domain/function is three levels — is that enough for MCTS to be useful, or do we need deeper branching?
- How do you define "cheap probes" generically? In software it's health checks and log queries. In a company it's asking people questions. What's the common abstraction?
- Can the symptom → hypothesis mappings be learned (Consolidate), or must they be authored?
- What's the rollout policy? Random rollouts work in Go because the game terminates. Diagnostic rollouts need a different termination condition.
- How does this relate to the existing Attend grid? Is this a new cell, or a specific instantiation of MCTS applied to a universal tree?
