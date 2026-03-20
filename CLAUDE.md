# Universal Diagnosis

Research exploration: cheap Attend for agents via MCTS-based diagnosis over a universal fault taxonomy.

## Context

- The Natural Framework defines six roles for any information system (Perceive/Cache/Filter/Attend/Remember/Consolidate)
- Blind-blind-merge is a working but expensive Attend implementation (portfolio solvers cell)
- This project explores MCTS (implicit redundancy, same row) as the cheaper alternative
- The key contribution: using the six roles as a universal fault tree, making diagnosis portable across domains

## Key files

- `README.md` — problem statement and open questions
- `taxonomy.md` — the universal fault taxonomy (sector/domain/function/role)
- `probes.md` — catalog of diagnostic probes per role

## Related

- Blog: `the-parts-bin.md` — algorithm catalog, Attend grid
- Blog: `blind-blind-merge.md` — the expensive solution this replaces
- Blog: `diagnosis-company.md` — applying diagnosis to companies
- Repo: `~/Documents/natural-framework/` — the framework itself
