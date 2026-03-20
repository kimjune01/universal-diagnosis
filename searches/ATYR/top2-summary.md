# ATYR Top-2 Search Reports (Event-Based)

## Report 1: Consolidate-A (backward pass — FDA/ClinicalTrials.gov)

11 events. Key trajectory:

| Date | Pipe | Status | Evidence |
|------|------|--------|----------|
| 2022-09-15 | write_substrate | functional | EFZO-FIT Phase 3 initiated (NCT05415137), OCS dose as primary |
| 2023-10-26 | write_substrate | functional | EFZO-CONNECT Phase 2 in SSc-ILD initiated (parallel track) |
| 2025-03-18 | read_outcomes | functional | FDA alignment on primary endpoint analysis plan via Type C |
| 2025-09-15 | read_outcomes | functional | Topline miss acknowledged honestly. Placebo response explanation, secondary signals highlighted. |
| 2025-09-30 | read_outcomes | functional | ERS Congress: secondary data presented in peer venue (KSQ-Lung p=0.0479, FAS p=0.0226) |
| 2025-06-04 | write_substrate | functional | EFZO-CONNECT interim: 3/4 diffuse SSc-ILD patients improved on mRSS |
| 2025-11-06 | batch_process | stressed | Q3 earnings: plans FDA meeting, no program discontinuation, analyst skepticism |
| 2026-02-03 | batch_process | functional | FDA accepts Type C meeting, mid-April 2026 |
| 2026-03-05 | batch_process | stressed | FY2025: $80.9M cash, no restructuring, endpoint pivot under consideration |
| 2026-03-20 | write_substrate | unknown | No new sarcoidosis trial registered. Pending FDA Type C meeting. |

**TRAUMA_CHECK**: EFZO-FIT Phase 3 miss (Sep 2025). No prior failure of same class. **same_class: no** — first Phase 3 for efzofitimod.

## Report 2: Cache-B (forward pass — SEC filings, financial media)

16 events. Key trajectory:

| Date | Pipe | Status | Evidence |
|------|------|--------|----------|
| 2020-01-06 | perceive_cache | functional | Kyorin Japan deal ($20M upfront + $155M milestones) |
| 2024-12-10 | cache_filter | functional | Third DSMB review: continue without modifications |
| 2025-03-06 | cache_filter | functional | Fourth DSMB: no safety concerns across 268 patients |
| 2025-07-31 | cache_filter | stressed | Shkreli shorts ATYR, predicts 80% crash, calls drug "really bad" |
| 2025-09-15 | filter_attend | broken | Phase 3 primary miss (OCS p=0.3313). Stock -83%. |
| 2025-09-30 | filter_attend | stressed | ERS: management reframes around QoL endpoints |
| 2025-10-13 | attend_remember | stressed | Securities class action filed |
| 2025-11-06 | attend_remember | stressed | Q3: $92.9M cash, ~3.5Q runway at burn rate, no restructuring |
| 2026-02-03 | attend_remember | unknown | FDA Type C meeting scheduled mid-April |
| 2026-03-05 | attend_remember | stressed | FY2025: $80.9M cash, ~4Q runway, new Phase 3 would need dilution |

## Key context from other agents (not in top 2)

**Cache-A**: Mechanism is solid (NRP2 on granuloma macrophages). Phase 1b/2a showed dose-dependent steroid reduction + QoL improvement. Delphi consensus (Oct 2025) validated KSQ-Lung as appropriate endpoint — field lacked standards when EFZO-FIT was designed.

**Consolidate-B**: Read_outcomes partially honest (acknowledged miss, but pivoted to secondaries in same breath). Shkreli's short preceded Phase 3 by 2 months. Stock trades near cash value (~$0.85-0.94). Analyst community skeptical. No leadership changes post-miss — board backs Shukla.

## Framework assessment for catalyst prediction

Our catalyst: **aTyr announces a new sarcoidosis clinical trial (any phase, any design) by 2026-09-30.**

The gating event is the mid-April FDA Type C meeting. Timeline chain:
- Type C meeting: mid-April 2026
- FDA minutes: within 30 days → mid-May
- 8-K disclosure: within 4 business days → late May
- Company decision + trial design: 1-3 months → June-August
- Announcement: by September 30

The consolidate stack assessment:
- read_outcomes: **functional** (honest reading, thorough secondary analysis, ERS presentation)
- batch_process: **functional but pending** (FDA engagement, no panic pivot, preserving capital)
- write_substrate: **pending** (no new trial registered, waiting for FDA guidance)

Contrast with QURE (also failed to get FDA approval path):
- QURE fought the FDA feedback → relationship collapsed → dying_dying
- ATYR is engaging the FDA constructively → outcome unknown → depends on meeting
