# Universal Fault Taxonomy

The diagnostic tree MCTS navigates. Every node is a pipe. Every pipe has the same structure. Scale doesn't matter until rock bottom.

## Recursive structure

```
Pipe
├── Cache stack (forward pass)
│   ├── Perceive → Cache  [pipe]
│   ├── Cache → Filter    [pipe]
│   ├── Filter → Attend   [pipe]
│   └── Attend → Remember [pipe]
└── Consolidate stack (backward pass)
    ├── Read outcomes      [pipe]
    ├── Batch process      [pipe]
    └── Write substrate    [pipe]
```

Each `[pipe]` in the tree has the same structure — two stacks, each containing pipes. The tree is self-similar at every level.

## Rock bottom

A pipe is a leaf when it can't be decomposed further:
- An atomic operation (single function call, single SQL query)
- A single API call to an external system
- A person making one decision
- A hardware sensor reading

Everything above rock bottom is the same recursive structure. No special treatment for "company-level" vs. "function-level" vs. "code-level" — the diagnostic algorithm doesn't distinguish scale.

## MCTS navigation

At any node, the agent asks:
1. **Which stack?** Cache or consolidate. (One cheap binary probe.)
2. **Which handoff/stage?** Narrow within the stack. (4 or 3 children.)
3. **Recurse.** The selected child is itself a pipe. Go to 1.

Terminate when the node is rock bottom — no further decomposition possible. The fault is localized.

## Branching factor

Uniform at every level:
- Stack split: 2
- Children per stack: 4 (cache) or 3 (consolidate)
- Depth: determined by the system's actual complexity, not by a predefined taxonomy

No need for sector/domain/function labels in the tree itself. Those are metadata on a node, useful for selecting priors and probe vocabularies, but the tree structure is purely recursive pipes.

## Entry point

The root pipe is whatever the agent is asked to diagnose — a company, a software system, a biological organism, a supply chain. The algorithm doesn't care. It sees a pipe.
