# Diagnostic Probes

A probe is a cheap question that narrows the fault tree. Organized by stack, then by fault site within each stack.

## Stack-level probe (the first question)

**"Is the output wrong now, or has it failed to improve over time?"**

- Wrong now → cache stack fault
- Same wrong as before → consolidate stack fault
- Both → cache stack first (can't learn if processing is broken)

This binary split is nearly free — it requires only comparing current output to historical output.

## Cache stack probes (forward pass)

Each probe targets a handoff between adjacent roles.

### Perceive → Cache handoff
**Failure mode**: Inputs arrive but aren't buffered or formatted correctly.
- Is the data source connected and responding?
- Are inputs arriving at expected frequency?
- Does the raw input match expected schema/format?
- Is there a mismatch between what's available and what's consumed?
- Latency between receipt and availability to next stage?

### Cache → Filter handoff
**Failure mode**: Data is buffered but bad candidates aren't rejected.
- Is there a queue/buffer between input and processing?
- Are messages being dropped under load?
- What's the acceptance rate? (too high = not filtering, too low = over-filtering)
- Are the rejection criteria current? (stale rules, outdated thresholds)

### Filter → Attend handoff
**Failure mode**: Candidates pass through but selection/ranking fails.
- Can you show me a recently rejected item — was rejection correct?
- Can you show me a recently accepted item — was acceptance correct?
- Is the top-ranked result actually the best? (spot check)
- Is there diversity in the selected set, or are picks redundant?
- Are the ranking criteria aligned with the actual objective?

### Attend → Remember handoff
**Failure mode**: Selection is correct but state doesn't persist.
- Is the selection bounded appropriately? (too many, too few)
- Does a write followed by a read return the same data?
- Is there data loss under concurrent access?
- Are retention policies correct? (keeping too much, deleting too soon)

## Consolidate stack probes (backward pass)

Each probe targets a stage of the learning loop.

### Remember → read (outcome collection)
**Failure mode**: Outcomes aren't being collected, or the wrong outcomes are collected.
- What outcomes are being recorded?
- Is the outcome signal aligned with the actual objective? (Goodhart risk)
- Are outcomes arriving at sufficient volume and frequency?
- Is there survivorship bias in what gets recorded?

### Batch process (learning execution)
**Failure mode**: Outcomes are collected but no learning happens.
- Is there a scheduled process that reads outcomes and computes updates?
- When did it last run? How long did it take?
- Are the feedback signals actually reaching the learning mechanism?
- Is the learning rate appropriate? (too fast = instability, too slow = stagnation)

### Write → substrate (parameter update)
**Failure mode**: Learning runs but updates don't land.
- Has behavior changed in response to recent feedback?
- Does the system perform better on repeated similar inputs over time?
- Are updates being applied atomically, or can partial writes corrupt state?
- Is there a rollback mechanism if an update degrades performance?

## Probe cost model

Probes vary in cost. MCTS should prefer cheaper probes early, escalating when cheap probes are ambiguous.

| Cost | Cache stack examples | Consolidate stack examples |
|------|---------------------|---------------------------|
| **Free** | Check logs, inspect config | Check cron/scheduler status |
| **Cheap** | Send test input, query DB | Compare this week vs. last week |
| **Moderate** | Synthetic workload, A/B test | Retrain on held-out data |
| **Expensive** | Instrument code, load test | Full feedback loop audit |

Key asymmetry: cache stack probes are mostly *spatial* (test one component now). Consolidate stack probes are mostly *temporal* (compare behavior across time).

## Common language

Every probe can be expressed as:

```
Given [pipe] in [function/domain/sector],
  stack: [cache | consolidate],
  site: [handoff or stage],
when [stimulus],
expect [response],
observe [actual].
```

The gap between expect and observe is the diagnostic signal.
