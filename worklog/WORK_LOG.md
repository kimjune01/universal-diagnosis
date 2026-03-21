# Work Log

## 2026-03-20

### 21:45 — Reader as blind-blind-merge attend step

Blog post presents framework view and analyst view side by side. The reader implicitly performs the blind-blind-merge attend step — we don't merge for them, we lay out two independent outputs and let them pick. The blog post is the merge interface. This is the division of intellect working as designed: skills automate Filter (reject what's wrong), human keeps Attend (select what's right). The two codex merge instances are truly blind to each other and to Shkreli. Shkreli is a public benchmark, not a merge partner. The reader is the final merger.

### 22:15 — Session complete: all artifacts published

**Published:**
- Blog post live at june.kim/diagnosis-biotech
- GitHub repo: github.com/kimjune01/universal-diagnosis with results.md, speculation.md, all diagnoses, SOAP notes, search reports, prereg
- Three Run 1 predictions timestamped: SPRB PASS (by Dec 31), ATYR PASS (by Sep 30), INMB FAIL (by Sep 30)

**Post-publication discussion:**
- INMB FAIL is consensus (Shkreli also bearish) — no edge, but selling calls captures theta if liquidity exists
- ATYR PASS is the edge case — framework disagrees with Shkreli and analyst community. If right, the framework sees something they don't. Cheap calls.
- speculation.md added to repo with trade thought experiments, clearly labeled not investment advice

**Endgame hypothesis (blog post seed, not published):**
If diagnosis becomes cheap enough, the information asymmetry inverts. Management spin has a shorter half-life. Companies with broken read_outcomes pipes get starved of capital sooner. Surviving companies are the ones that actually learn. The market is the environment, diagnosis is the selection pressure, honesty becomes thermodynamically favorable (Landauer: reconstructing the signal costs less than erasing it). Consolidation follows — companies that can't self-correct get acquired by ones that can, faster.

**Next:**
- Wait for catalysts: ATYR/INMB by Sep 30, SPRB by Dec 31
- Leading indicators: ATYR FDA Type C meeting mid-April, INMB MHRA pre-MAA feedback May
- Future work: vol backtest (IV vs realized around catalyst dates), insider transaction signals (Form 4 events in temporal graph)

### 22:45 — Backtest prereg simplified, dashboard built, audit trail formalized

Simplified the backtest from "scrape 300 Phase 3 readouts" to "follow Shkreli's public positions as they come." If he tweets it, we run it. If he stops covering it, we stop too. N grows organically — 5-10/year, significance may take years, dashboard shows convergence in real time.

Key design decisions:
- Selection rule is Shkreli's posts, not our choice. Eliminates cherry-picking.
- Full audit trail required: Shkreli source URL → 4 search reports → 2 SOAP notes → diagnosis → ground truth URL. Every event in the temporal graph has a source_url.
- Dashboard (dashboard.html) polls scorecard.json every 30s. Shows running accuracy, p-value vs 50% base rate, convergence bar at N>=10.
- export_scorecard.py regenerates JSON from DB after each resolution.
- Cost: ~$1/company in API calls, $5-15/year total.

Also discussed: if analysis becomes cheap, markets force companies into honesty. Spin is an adaptation to information-expensive environments. In information-cheap environments, it's maladaptive. The market is the selection pressure. Honest consolidate stacks survive. This is a blog post seed for later — the Landauer connection (erasing failure signals costs more than reconstructing them).

### 23:15 — Codex data collection review, snapshot-only baseline added

Codex reviewed the prereg against the hypothesis "seven-pipe temporal graph beats snapshot expert." Key finding: **we had no snapshot-only baseline.** Without it, we can't claim the temporal ordering adds value — we'd only be showing "our process produces scorable calls."

Changes to prereg-backtest.md:
- **Three arms per company**: temporal-graph prediction, snapshot-only prediction (same pipes, no ordering), analyst prediction
- **Three hypotheses**: H1 temporal > snapshot (McNemar's), H2 temporal > analyst (McNemar's), H3 vol mispricing
- **Graph-derived features**: recurrence count, transition count, repair latency, pipe coverage, event density, failure-to-repair path. Computed from events we already collect.
- **Confidence levels**: high/medium/low for framework (based on merge agreement), inferred for analyst (from language strength)
- The CAPR smoke test (static framing) is retroactively our first snapshot-only baseline — the controlled comparison we did by accident.

Dashboard MVP also built this session: FastAPI + React, burger menu, health LED, event timeline with time travel, pipe status panel, prediction card, runway bar. Needs events loaded into DB to populate.

### 23:45 — Prereg finalized: three-arm backtest, schema aligned, codex approved

Major changes in final stretch:

**Schema overhaul**: dropped `analyst_call` table entirely. Analyst prediction is now a third arm in the `prediction` table (arm='temporal'|'snapshot'|'analyst'). All three arms scored against same ground truth, same catalyst, same window.

**Phase 1 backtest added**: pull every qualifying Shkreli biotech position from May 2022-Dec 2025. Build temporal graphs from records dated before each catalyst. Score against known outcomes. Gives N=20-30 immediately.

**Codex blockers resolved** (two rounds):
- Position definition: 4 mechanical rules, deduplication (first directional per ticker), canonical source priority
- Snapshot classification: exhaustive 2×2 table (cache status × consolidate status → category → direction). No "etc."
- Analyst-to-catalyst mapping: 4 rules for generic bull/bear → specific catalyst
- Eviction: dropped stale rule, catalyst window runs to completion
- Schema/prereg alignment: both preregs now reference same three-arm model

**Exploratory hypotheses logged** (deferred until N=30+):
- Runway × bucket interaction: among living_dying companies, do those with > 8q runway outperform those with < 4q?
- Per-bucket hit rates: which category predicts best?
- Graph feature analysis: do recurrence count, repair latency, pipe coverage predict accuracy within buckets?

**User's personal hypothesis**: "given enough runway, a learning company will outperform." Testable as living_dying × high runway vs. living_dying × low runway.

**What's next**:
- Load events from search reports into DB (parser needed)
- Phase 1 discovery: pull Shkreli's historical biotech positions 2022-2025
- Process Phase 1 companies through three-arm pipeline
- Dashboard v2 frontend polish

### 00:15 — Prereg approved by codex, ready to execute Phase 1

Final three schema blockers fixed: run enum (phase1/phase2/pilot_run0/pilot_run1), UNIQUE(company_id, arm, catalyst) constraint, graph features + confidence fields on prediction row. Codex confirmed no remaining blockers.

Key discussion points before shipping:
- Bare LLM arm considered and rejected as redundant — snapshot-only already isolates the temporal ordering question. Adding a third comparison dilutes McNemar's power at N=25.
- Expected surprises: snapshot might tie temporal (Peters is decorative), living_dying might be hardest bucket (cash moderates), Shkreli might just be good (strong comparator), analyst-to-catalyst mapping might be lossy.
- Theory-is-load-bearing already showed framework improves diagnostic quality. This pilot tests whether that translates to predictive accuracy on real binary outcomes. Cross-domain generalization is a separate experiment.

**Status: prereg locked, schema aligned, ready for Phase 1 discovery.**

### 00:30 — Phase 1 discovery started

Phase 1 discovery started. Initial search found ~8-10 qualifying Shkreli post-prison biotech positions (May 2022-Dec 2025). Five already in pilot (CAPR, QURE, SPRB, ATYR, INMB). New candidates: SAVA (short Nov 2024, Phase 3 failed, stock -86% — clear add), GALT (short Dec 2024, needs research), AVXL (excluded — "don't know when" fails position definition rule #2). Pool is smaller than the 20-30 estimated in prereg. Per prereg rules: discovery must be exhaustive before freezing the list. Need deeper search of X archive, YouTube, interviews next session. No processing until list is frozen.
