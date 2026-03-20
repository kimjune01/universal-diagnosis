# CAPR Top-2 Search Reports (Event-Based)

## Report 1: Consolidate-A (backward pass — FDA/ClinicalTrials.gov)

22 events across read_outcomes, batch_process, write_substrate. Key trajectory:

| Date | Pipe | Status | Evidence |
|------|------|--------|----------|
| 2017-05-12 | read_outcomes | broken | ALLSTAR futility on primary (scar reduction p=0.65) |
| 2017-05-12 | batch_process | functional | Same-day pivot announcement to DMD |
| 2017-07-07 | write_substrate | functional | Janssen drops option, Capricor retains all rights |
| 2018-01-23 | write_substrate | functional | HOPE-2 posted: IV route, multi-dose, double-blind |
| 2018-02-05 | batch_process | functional | FDA grants RMAT designation |
| 2019-01-22 | read_outcomes | functional | RMAT meeting: FDA supports PUL 2.0, advises EOP meeting |
| 2024-08-07 | batch_process | functional | Pre-BLA meeting positive; strategy: file on HOPE-2/OLE + natural history |
| 2024-09-24 | write_substrate | functional | Decision to file BLA without waiting for HOPE-3 |
| 2024-10-09 | write_substrate | functional | Rolling BLA initiated |
| 2025-01-02 | write_substrate | functional | BLA submission complete, $10M Nippon milestone |
| 2025-03-04 | batch_process | functional | BLA accepted, Priority Review, PDUFA Aug 31 2025 |
| 2025-05-13 | batch_process | stressed | Mid-cycle "no deficiencies" but AdCom planned (uncertainty signal) |
| 2025-07-11 | read_outcomes | broken | CRL: "does not meet substantial evidence of effectiveness" |
| 2025-07-11 | batch_process | functional | Same-day plan to resubmit with HOPE-3 data |
| 2025-08-11 | write_substrate | repaired | Type A meeting: all 483s resolved, HOPE-3 protocol amendment |
| 2025-11-10 | batch_process | repaired | FDA supports HOPE-3 as "additional study" for CRL |
| 2025-12-03 | read_outcomes | repaired | HOPE-3 topline positive: PUL v2.0 p=0.03, LVEF p=0.04 |
| 2025-12-05 | write_substrate | functional | $150M offering for commercialization |
| 2026-03-10 | write_substrate | repaired | FDA lifts CRL, PDUFA Aug 22 2026 |
| 2026-03-12 | batch_process | functional | FY2025 results, $318M cash, MDA late-breaking data |

**TRAUMA_CHECK**: ALLSTAR (2017, scientific/indication failure) vs CRL (2025, regulatory/evidence packaging). **same_class: no**. Different failure types — wrong indication vs. insufficient evidence for approval.

## Report 2: Cache-A (forward pass — ClinicalTrials.gov/PubMed)

16 events across perceive_cache, cache_filter, filter_attend, attend_remember. Key trajectory:

| Date | Pipe | Status | Evidence |
|------|------|--------|----------|
| 2012-02-14 | perceive_cache | functional | CADUCEUS: intracoronary CDCs reach myocardium, reduce scar |
| 2014-09-01 | perceive_cache | functional | Xie: CDCs need direct cell contact via beta-1 integrin |
| 2018-03-01 | cache_filter | functional | Rogers: CDC exosomes reproduce benefits, partial dystrophin restoration |
| 2019-02-19 | perceive_cache | functional | HOPE-1: intracoronary CDCs reach cardiac+skeletal targets in DMD |
| 2019-02-19 | cache_filter | functional | HOPE-1: safety comparable between groups |
| 2019-04-04 | perceive_cache | functional | Smith: IV CDCs reach cardiac+skeletal targets in mdx mice |
| 2020-09-21 | filter_attend | broken | ALLSTAR publication: primary endpoint failed (scar size wrong readout) |
| 2020-05-12 | cache_filter | functional | COVID compassionate use: IV well tolerated in critically ill |
| 2022-01-01 | perceive_cache | functional | Ciullo: CDC EVs accumulate in heart per mg after IV |
| 2022-03-12 | filter_attend | repaired | HOPE-2: new endpoint (PUL 1.2) captures signal, p=0.014 |
| 2022-03-12 | cache_filter | stressed | HOPE-2: 37.5% hypersensitivity rate (3/8 treated) |
| 2025-02-24 | attend_remember | functional | HOPE-2 OLE: 13 patients, up to 20 infusions over 60 months |
| 2025-10-29 | perceive_cache | functional | Potency assay links manufacturing to clinical outcome |

**Key transition**: filter_attend went broken (2020, ALLSTAR wrong endpoint) → repaired (2022, HOPE-2 right endpoint). This is the same transition the smoke test found, but now grounded in publication dates.

## Consolidate-B trauma recurrence (alternate view, not in top 2)

**same_class: yes** — CRL and securities fraud class action both stem from the gap between management's characterization of data adequacy and FDA's actual assessment. This disagrees with Consolidate-A's "no" — a genuine divergence the merge should surface.
