OpenAI Codex v0.114.0 (research preview)
--------
workdir: /Users/junekim/Documents/universal-diagnosis
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 019d0cc2-b11f-72b2-8a66-42f4d0336695
--------
user
Merge these event-based search reports into a SOAP note for uniQure (QURE). Run 0 retrospective — outcome known: AMT-130 topline positive Sep 2025, but FDA reversed in Nov 2025, demanded Phase 3 in Jan 2026, then publicly accused company of pushing distorted data in Mar 2026. Stock -84% from highs. Shkreli was long, sold Nov 2025 before the break.

Company IS the consolidate stack for AMT-130. Output: S (one paragraph), O (event timeline table + transitions), A (trajectory category: living_well/living_dying/dying_pivoted/dying_dying, trauma recurrence), P (prediction record: Company, Type, Category, Direction PASS/FAIL, Catalyst, Resolution source, Window start, Window end, Pass condition, Reasoning), Refs.
mcp startup: no servers
codex
I’m verifying the AMT-130 event sequence and the specific outcome dates before drafting the SOAP note. I’ll use primary company materials where possible and then consolidate the timeline, category judgment, and prediction record.
🌐 Searching the web...
🌐 Searched: uniQure AMT-130 topline positive September 2025 press release
🌐 Searching the web...
🌐 Searched: site:uniqure.com AMT-130 January 2026 Phase 3 required
🌐 Searching the web...
🌐 Searched: site:uniqure.com March 2 2026 uniQure AMT-130 Type A meeting minutes
🌐 Searching the web...
🌐 Searched: "Federal Health Officials Attack Rare-Disease Drug, Say Company Lied"
🌐 Searching the web...
🌐 Searched: finance: QURE
codex
I have the core dates now: September 24, 2025 topline, November 3, 2025 FDA setback disclosure, January 30, 2026 Type A meeting later disclosed on March 2, 2026, and the March 5-6, 2026 public FDA rebuke. I’m tightening the sourcing for stock drawdown and then I’ll format the note exactly as requested.
🌐 Searching the web...
🌐 Searched: finance: QURE
🌐 Searching the web...
🌐 Searched: QURE stock March 2026 high 67.69 current 9.80
🌐 Searching the web...
🌐 Searched: "i sold" Martin Shkreli November 3 2025 uniQure
codex
**S**  
uniQure became, in practice, an AMT-130 single-asset equity story after its September 24, 2025 Huntington’s topline: management framed the Phase I/II readout as pivotal, statistically persuasive, and aligned with an accelerated BLA path, which drove a sharp repricing higher. That thesis then unraveled in stages: on November 3, 2025 the company disclosed FDA no longer agreed the external-control comparison could serve as primary evidence for a BLA; on March 2, 2026 uniQure disclosed final minutes from a January 30, 2026 Type A meeting in which FDA explicitly said the Phase I/II package was insufficient and strongly recommended a prospective randomized, double-blind, sham-controlled Phase 3-style study; and on March 5-6, 2026 the dispute became reputationally toxic when senior U.S. health officials publicly attacked the program and accused the company of distorted/manipulated presentation. From the post-readout highs in late September/early October 2025 to roughly $10-12 in early March 2026, QURE lost about 84% to 86% of value. Martin Shkreli appears to have been long into the September move and publicly claimed he sold on November 3, 2025 before the deeper break.

**O**

| Date | Event | Evidence / Market Meaning | Transition |
|---|---|---|---|
| June 2, 2025 | FDA interaction supported cUHDRS as registrational intermediate endpoint and external-control-based primary analysis plan | Regulatory setup looked supportive for accelerated approval | `setup -> optimism` |
| September 24, 2025 | uniQure reported positive topline from pivotal Phase I/II AMT-130 study and said it planned BLA submission in Q1 2026 | Company positioned AMT-130 as approvable on existing package; stock surged | `optimism -> euphoria` |
| November 3, 2025 | uniQure disclosed FDA, after pre-BLA interaction, no longer agreed Phase I/II plus external control may be adequate as primary evidence for BLA | Core approval thesis broke; stock fell about 49% in one session | `euphoria -> regulatory fracture` |
| January 30, 2026 | Type A meeting held with FDA | Formal escalation from ambiguity to dispute over evidentiary standard | `regulatory fracture -> adjudication` |
| March 2, 2026 | uniQure disclosed final Type A minutes: FDA said Phase I/II vs external control was not sufficient and strongly recommended a prospective randomized, double-blind, sham surgery-controlled study | De facto requirement for Phase 3; timeline and capital intensity reset by years | `adjudication -> thesis reset` |
| March 3, 2026 | STAT reported senior FDA official said agency was not convinced AMT-130 showed therapeutic benefit | Agency skepticism moved from procedural to substantive | `thesis reset -> credibility damage` |
| March 5-6, 2026 | Reuters/WSJ/STAT reported senior FDA/HHS officials publicly called AMT-130 a failed product and accused uniQure of distorted/manipulated comparison / misleading statements | Conflict became public and reputational; not just delay, but trust impairment | `credibility damage -> trauma event` |

**A**  
**Trajectory category:** `dying_pivoted`  

uniQure is not obviously insolvent or dead as a corporation, but the original AMT-130 equity thesis failed. Because the company had become the consolidated AMT-130 stack, the loss of the external-control accelerated path was not a routine setback; it invalidated the central timing, approval, and valuation bridge that justified the prior rerating. The March 2026 public rebuke matters more than a normal CRL-style delay because it damages management-regulator credibility in addition to delaying the asset. The remaining path is a pivot: fund and design a sham-controlled Phase 3-type study, preserve cash runway, and hope other pipeline assets eventually matter enough to dilute AMT-130 concentration.

**Trauma recurrence:** `high`  
Pattern recurrence is clear: rare-disease/gene-therapy companies leaning on small studies, external controls, and accelerated-approval framing can experience sudden regulator re-interpretation, followed by financing, timeline, and credibility trauma. Here the recurrence is intensified by the company having previously described FDA alignment in June 2025 and then suffering a visible reversal by November 2025 and a public denunciation by March 2026.

**P**

| Company | Type | Category | Direction PASS/FAIL | Catalyst | Resolution source | Window start | Window end | Pass condition | Reasoning |
|---|---|---|---|---|---|---|---|---|---|
| uniQure (QURE) | Retrospective event-based call | Regulatory / single-asset thesis | `FAIL` | AMT-130 transitions from positive topline to durable BLA path | uniQure Sept. 24, 2025 PR; uniQure Nov. 3, 2025 update; uniQure Mar. 2, 2026 8-K / PR; STAT Mar. 3 and Mar. 6, 2026; Reuters Mar. 5, 2026 | 2025-09-24 | 2026-03-06 | FDA continues to accept Phase I/II plus external control as primary evidence, no Phase 3 requirement emerges, and no public regulator-company credibility rupture occurs | Topline efficacy was real enough to create upside, but the investable thesis depended on regulatory acceptance of the external-control construct. Once FDA withdrew that acceptance and later publicly attacked the company’s framing, the thesis failed even if AMT-130 still retains biological possibility. |

**Refs**  
- uniQure, June 2, 2025 regulatory update on AMT-130: https://uniqure.gcs-web.com/news-releases/news-release-details/uniqure-provides-regulatory-update-amt-130-huntingtons-disease  
- uniQure, September 24, 2025 positive topline: https://uniqure.gcs-web.com/news-releases/news-release-details/uniqure-announces-positive-topline-results-pivotal-phase-iii  
- uniQure, November 10, 2025 Q3 update summarizing the November 3 FDA setback: https://www.globenewswire.com/news-release/2025/11/10/3184405/0/en/p.html  
- International Huntington Association repost of uniQure’s November 3, 2025 regulatory update: https://huntington-disease.org/2025/11/03/uniqure-provides-regulatory-update-on-amt-130-for-huntingtons-disease/  
- uniQure March 2, 2026 8-K: https://www.sec.gov/Archives/edgar/data/1590560/000110465926021890/qure-20260302x8k.htm  
- uniQure March 2, 2026 AMT-130 regulatory update exhibit: https://www.sec.gov/Archives/edgar/data/1590560/000110465926021890/qure-20260302xex99d2.htm  
- uniQure 2025 10-K discussion of December 2025 / March 2026 FDA position: https://www.sec.gov/Archives/edgar/data/0001590560/000110465926021898/qure-20251231x10k.htm  
- STAT, March 3, 2026: https://www.statnews.com/2026/03/03/uniqure-huntingtons-treatment-fda-official-comments/  
- STAT, March 6, 2026: https://www.statnews.com/2026/03/06/fda-uniqure-rare-disease-huntingtons/  
- Reuters, March 5, 2026 summary via Yahoo Finance: https://finance.yahoo.com/news/fda-official-calls-uniqures-huntingtons-194738991.html  
- Shkreli sale claim cited in ZeroHedge, December 16, 2025: https://www.zerohedge.com/news/2025-12-16/big-news-biotech

If you want, I can convert this into a tighter investment-memo format or a JSON schema next.
tokens used
29,388
**S**  
uniQure became, in practice, an AMT-130 single-asset equity story after its September 24, 2025 Huntington’s topline: management framed the Phase I/II readout as pivotal, statistically persuasive, and aligned with an accelerated BLA path, which drove a sharp repricing higher. That thesis then unraveled in stages: on November 3, 2025 the company disclosed FDA no longer agreed the external-control comparison could serve as primary evidence for a BLA; on March 2, 2026 uniQure disclosed final minutes from a January 30, 2026 Type A meeting in which FDA explicitly said the Phase I/II package was insufficient and strongly recommended a prospective randomized, double-blind, sham-controlled Phase 3-style study; and on March 5-6, 2026 the dispute became reputationally toxic when senior U.S. health officials publicly attacked the program and accused the company of distorted/manipulated presentation. From the post-readout highs in late September/early October 2025 to roughly $10-12 in early March 2026, QURE lost about 84% to 86% of value. Martin Shkreli appears to have been long into the September move and publicly claimed he sold on November 3, 2025 before the deeper break.

**O**

| Date | Event | Evidence / Market Meaning | Transition |
|---|---|---|---|
| June 2, 2025 | FDA interaction supported cUHDRS as registrational intermediate endpoint and external-control-based primary analysis plan | Regulatory setup looked supportive for accelerated approval | `setup -> optimism` |
| September 24, 2025 | uniQure reported positive topline from pivotal Phase I/II AMT-130 study and said it planned BLA submission in Q1 2026 | Company positioned AMT-130 as approvable on existing package; stock surged | `optimism -> euphoria` |
| November 3, 2025 | uniQure disclosed FDA, after pre-BLA interaction, no longer agreed Phase I/II plus external control may be adequate as primary evidence for BLA | Core approval thesis broke; stock fell about 49% in one session | `euphoria -> regulatory fracture` |
| January 30, 2026 | Type A meeting held with FDA | Formal escalation from ambiguity to dispute over evidentiary standard | `regulatory fracture -> adjudication` |
| March 2, 2026 | uniQure disclosed final Type A minutes: FDA said Phase I/II vs external control was not sufficient and strongly recommended a prospective randomized, double-blind, sham surgery-controlled study | De facto requirement for Phase 3; timeline and capital intensity reset by years | `adjudication -> thesis reset` |
| March 3, 2026 | STAT reported senior FDA official said agency was not convinced AMT-130 showed therapeutic benefit | Agency skepticism moved from procedural to substantive | `thesis reset -> credibility damage` |
| March 5-6, 2026 | Reuters/WSJ/STAT reported senior FDA/HHS officials publicly called AMT-130 a failed product and accused uniQure of distorted/manipulated comparison / misleading statements | Conflict became public and reputational; not just delay, but trust impairment | `credibility damage -> trauma event` |

**A**  
**Trajectory category:** `dying_pivoted`  

uniQure is not obviously insolvent or dead as a corporation, but the original AMT-130 equity thesis failed. Because the company had become the consolidated AMT-130 stack, the loss of the external-control accelerated path was not a routine setback; it invalidated the central timing, approval, and valuation bridge that justified the prior rerating. The March 2026 public rebuke matters more than a normal CRL-style delay because it damages management-regulator credibility in addition to delaying the asset. The remaining path is a pivot: fund and design a sham-controlled Phase 3-type study, preserve cash runway, and hope other pipeline assets eventually matter enough to dilute AMT-130 concentration.

**Trauma recurrence:** `high`  
Pattern recurrence is clear: rare-disease/gene-therapy companies leaning on small studies, external controls, and accelerated-approval framing can experience sudden regulator re-interpretation, followed by financing, timeline, and credibility trauma. Here the recurrence is intensified by the company having previously described FDA alignment in June 2025 and then suffering a visible reversal by November 2025 and a public denunciation by March 2026.

**P**

| Company | Type | Category | Direction PASS/FAIL | Catalyst | Resolution source | Window start | Window end | Pass condition | Reasoning |
|---|---|---|---|---|---|---|---|---|---|
| uniQure (QURE) | Retrospective event-based call | Regulatory / single-asset thesis | `FAIL` | AMT-130 transitions from positive topline to durable BLA path | uniQure Sept. 24, 2025 PR; uniQure Nov. 3, 2025 update; uniQure Mar. 2, 2026 8-K / PR; STAT Mar. 3 and Mar. 6, 2026; Reuters Mar. 5, 2026 | 2025-09-24 | 2026-03-06 | FDA continues to accept Phase I/II plus external control as primary evidence, no Phase 3 requirement emerges, and no public regulator-company credibility rupture occurs | Topline efficacy was real enough to create upside, but the investable thesis depended on regulatory acceptance of the external-control construct. Once FDA withdrew that acceptance and later publicly attacked the company’s framing, the thesis failed even if AMT-130 still retains biological possibility. |

**Refs**  
- uniQure, June 2, 2025 regulatory update on AMT-130: https://uniqure.gcs-web.com/news-releases/news-release-details/uniqure-provides-regulatory-update-amt-130-huntingtons-disease  
- uniQure, September 24, 2025 positive topline: https://uniqure.gcs-web.com/news-releases/news-release-details/uniqure-announces-positive-topline-results-pivotal-phase-iii  
- uniQure, November 10, 2025 Q3 update summarizing the November 3 FDA setback: https://www.globenewswire.com/news-release/2025/11/10/3184405/0/en/p.html  
- International Huntington Association repost of uniQure’s November 3, 2025 regulatory update: https://huntington-disease.org/2025/11/03/uniqure-provides-regulatory-update-on-amt-130-for-huntingtons-disease/  
- uniQure March 2, 2026 8-K: https://www.sec.gov/Archives/edgar/data/1590560/000110465926021890/qure-20260302x8k.htm  
- uniQure March 2, 2026 AMT-130 regulatory update exhibit: https://www.sec.gov/Archives/edgar/data/1590560/000110465926021890/qure-20260302xex99d2.htm  
- uniQure 2025 10-K discussion of December 2025 / March 2026 FDA position: https://www.sec.gov/Archives/edgar/data/0001590560/000110465926021898/qure-20251231x10k.htm  
- STAT, March 3, 2026: https://www.statnews.com/2026/03/03/uniqure-huntingtons-treatment-fda-official-comments/  
- STAT, March 6, 2026: https://www.statnews.com/2026/03/06/fda-uniqure-rare-disease-huntingtons/  
- Reuters, March 5, 2026 summary via Yahoo Finance: https://finance.yahoo.com/news/fda-official-calls-uniqures-huntingtons-194738991.html  
- Shkreli sale claim cited in ZeroHedge, December 16, 2025: https://www.zerohedge.com/news/2025-12-16/big-news-biotech

If you want, I can convert this into a tighter investment-memo format or a JSON schema next.
