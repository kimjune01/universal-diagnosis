OpenAI Codex v0.114.0 (research preview)
--------
workdir: /Users/junekim/Documents/universal-diagnosis
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 019d0cad-fd3f-7710-89fc-11fa5e79ef3e
--------
user
Merge these event-based search reports into a SOAP note for CAPR (Run 0, retrospective, HOPE-3 succeeded Dec 2025). Shkreli shorted Nov 2025, was wrong. Company IS the consolidate stack. Output: S (one paragraph), O (event timeline table + transitions), A (trajectory category: living_well/living_dying/dying_pivoted/dying_dying, trauma recurrence disagreement), P (prediction record with all fields: Company, Type, Category, Direction, Catalyst, Resolution source, Window start, Window end, Pass condition, Reasoning), Refs.
mcp startup: no servers
codex
I’m locating the event-based search reports for CAPR Run 0 and the related HOPE-3/Shkreli materials first, then I’ll consolidate them into the requested SOAP structure.
exec
/bin/zsh -lc 'rg --files .' in /Users/junekim/Documents/universal-diagnosis succeeded in 0ms:
./init_db.py
./CLAUDE.md
./biotech.md
./main.py
./design.md
./prompts/cache-agent.md
./prompts/merge-agent.md
./prompts/consolidate-agent.md
./prereg.md
./notes/CAPR/soap-a.md
./notes/CAPR/soap-b.md
./diagnose.py
./worklog.md
./README.md
./smoke-test/CAPR/cache-a.md
./smoke-test/CAPR/top2-summary.md
./smoke-test/CAPR/soap-a.md
./smoke-test/CAPR/consolidate-a.md
./smoke-test/CAPR/consolidate-b.md
./smoke-test/CAPR/soap-b.md
exec
/bin/zsh -lc 'rg -n "CAPR|HOPE-3|Shkreli|consolidate stack|Run 0|retrospective" .' in /Users/junekim/Documents/universal-diagnosis succeeded in 0ms:
./init_db.py:1:"""Initialize the database and seed with Shkreli's biotech targets."""
./init_db.py:18:    # Seed companies from Shkreli's 2025-2026 positions
./init_db.py:20:        ("CAPR", "Capricor Therapeutics", "biotech",
./init_db.py:21:         "Shkreli shorted, said HOPE-3 'will not work'. Stock +440% on positive Phase 3. Admitted 'bad call'. Run 0 demonstration."),
./init_db.py:23:         "Shkreli long, targets $500, says TA-ERT 'will be approved'. BLA submission expected Q4 2026. Run 1 forward."),
./init_db.py:25:         "Shkreli was long on AMT-130 (Huntington's gene therapy), saw 5-10x, sold Nov 2025. Run 0 demonstration."),
./init_db.py:27:         "Shkreli short, predicted 80% crash. FDA Type C meeting mid-April 2026. Run 1 forward."),
./init_db.py:29:         "Shkreli predicted 90% drop. MAA submission mid-summer 2026. Run 1 forward."),
./init_db.py:38:    # Seed CAPR pipe topology (stable across time)
./init_db.py:39:    capr_id = db.execute("SELECT id FROM company WHERE ticker = 'CAPR'").fetchone()[0]
./init_db.py:58:    # Seed known traumas for CAPR
./init_db.py:64:        (capr_id, None, "Shkreli publishes 46-page short report, stock drops 17%",
./init_db.py:65:         "2025-11-24", "https://x.com/MartinShkreli/status/1992971976294498581", "analyst_short_attack"),
./init_db.py:66:        (capr_id, None, "HOPE-3 Phase 3 positive topline: PUL v2.0 p=0.029, LVEF p=0.041, stock +440%",
./CLAUDE.md:3:Generate falsifiable predictions from the Natural Framework. Biotech pilot: head-to-head with Martin Shkreli's public calls.
./CLAUDE.md:7:Legitimize the Natural Framework by publishing timestamped predictions that outperform domain expert analysts. The molecule is the pipe, the company is its consolidate stack.
./CLAUDE.md:31:uv run python diagnose.py timeline CAPR       # show event timeline per pipe
./CLAUDE.md:32:uv run python diagnose.py transitions CAPR    # show status changes only
./biotech.md:5:The molecule is the pipe. The company is its consolidate stack.
./biotech.md:82:A pharma giant acquiring a biotech is buying a consolidate stack. The acquirer's own backward pass is too slow for a novel mechanism — its Read/Process/Write cycle takes decades. The biotech has already iterated the molecule through several cycles. The acquisition imports a faster consolidate stack.
codex
I found the CAPR event-based materials in `searches/CAPR/` and the existing merge prompt in `notes/CAPR/soap-a.md`. I’m reading the top-2 summary and the merged prompt body now to extract the exact event timeline, disagreement, and prediction fields.
exec
/bin/zsh -lc "sed -n '1,240p' notes/CAPR/soap-a.md" in /Users/junekim/Documents/universal-diagnosis succeeded in 0ms:
OpenAI Codex v0.114.0 (research preview)
--------
workdir: /Users/junekim/Documents/universal-diagnosis
model: gpt-5.4
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 019d0cac-8e81-7e42-94c7-9febe6a4021d
--------
user
Merge these two event-based search reports into a SOAP note for Capricor Therapeutics (CAPR). This is Run 0 (retrospective demonstration — outcome known: HOPE-3 succeeded Dec 2025, stock +440%). Shkreli shorted Nov 2025, was wrong.

The company IS the consolidate stack for the molecule. The temporal graph grows one event at a time — each event is a public record with an archival date.

SOAP format:
S: What company/analysts said (one paragraph)
O: Merged event timeline table (Date | Pipe | Status | Evidence), then highlight transitions
A: Framework diagnosis — which pipes changed status, which stack drove the change, trauma recurrence result, trajectory category (living_well / living_dying / dying_pivoted / dying_dying)
exec
/bin/zsh -lc "sed -n '1,260p' searches/CAPR/top2-summary.md" in /Users/junekim/Documents/universal-diagnosis succeeded in 0ms:
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
exec
/bin/zsh -lc "sed -n '1,260p' searches/CAPR/consolidate-b.md" in /Users/junekim/Documents/universal-diagnosis succeeded in 0ms:
{"parentUuid":null,"isSidechain":true,"promptId":"bb1102f1-2068-4d12-b97b-1bf92da44543","agentId":"a518bc4e78426ebc2","type":"user","message":{"role":"user","content":"You are Instance B of the Consolidate Stack Search Agent. You are diagnosing the BACKWARD PASS of Capricor Therapeutics (CAPR). The company IS the consolidate stack for the molecule Deramiocel (CAP-1002).\n\nThe consolidate stack has three stages:\n1. read_outcomes: Did management acknowledge results honestly? Spin vs. honest reading?\n2. batch_process: What strategic decisions followed? New hires, new expertise, advisory board changes?\n3. write_substrate: What concrete changes are visible from outside? Manufacturing, partnerships, regulatory strategy?\n\nYOUR DATA SOURCES: Conference presentations, analyst reports, earnings calls, and financial media only. Use presentation/publication dates as source_date.\n\nOUTPUT FORMAT — for each relevant public record, output:\n\nEVENT:\n  pipe: [stage name]\n  source_date: [YYYY-MM-DD]\n  status: [functional | broken | stressed | repaired | unknown]\n  evidence: [one paragraph]\n  source_url: [URL]\n\nAfter all events, output:\n\nTRAUMA_CHECK:\n  failure_1: [description]\n  failure_1_date: [YYYY-MM-DD]\n  failure_1_source: [URL]\n  failure_2: [description or \"none\"]\n  failure_2_date: [YYYY-MM-DD or \"n/a\"]\n  failure_2_source: [URL or \"n/a\"]\n  same_class: [yes | no | unclear]\n  reasoning: [one sentence]\n\nRULES:\n- Every EVENT must have a real archival date. No estimates.\n- \"repaired\" means a prior event on the same pipe had status broken or stressed\n- Order chronologically\n- Do NOT make predictions\n- Search for: Capricor earnings calls and press releases (2018-2026), MDA/AHA/ACC conference presentations, CMO hire (Michael Binks May 2025), Nippon Shinyaku partnership, Shkreli's 46-page short report (Nov 2025) and his specific critique, securities fraud class action (Aug 2025)"},"uuid":"a94d7da5-0d36-48d8-917b-76b11d3dd9fb","timestamp":"2026-03-20T19:06:45.601Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"a94d7da5-0d36-48d8-917b-76b11d3dd9fb","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_016dtRgn5fweLPC7Gvwqme3a","type":"message","role":"assistant","content":[{"type":"text","text":"\n\nI'll systematically search for public records on Capricor Therapeutics' backward pass (consolidate stack) for Deramiocel/CAP-1002. Let me gather information from multiple sources."}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":3671,"cache_read_input_tokens":7486,"cache_creation":{"ephemeral_5m_input_tokens":3671,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbY2Z8VAH5RnsiHpFm","type":"assistant","uuid":"b0fd81a7-f5a0-4c7a-a96f-ecbf9fee09c4","timestamp":"2026-03-20T19:06:50.299Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"b0fd81a7-f5a0-4c7a-a96f-ecbf9fee09c4","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_016dtRgn5fweLPC7Gvwqme3a","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_01D96nuk4dEbGTiseJW5tXzu","name":"ToolSearch","input":{"query":"select:WebSearch,WebFetch","max_results":2},"caller":{"type":"direct"}}],"stop_reason":"tool_use","stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":3671,"cache_read_input_tokens":7486,"output_tokens":126,"server_tool_use":{"web_search_requests":0,"web_fetch_requests":0},"service_tier":"standard","cache_creation":{"ephemeral_1h_input_tokens":0,"ephemeral_5m_input_tokens":3671},"inference_geo":"","iterations":[],"speed":"standard"}},"requestId":"req_011CZErbY2Z8VAH5RnsiHpFm","type":"assistant","uuid":"1c5d3101-b614-4046-940c-2c86949656f2","timestamp":"2026-03-20T19:06:50.784Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"1c5d3101-b614-4046-940c-2c86949656f2","isSidechain":true,"promptId":"bb1102f1-2068-4d12-b97b-1bf92da44543","agentId":"a518bc4e78426ebc2","type":"user","message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"toolu_01D96nuk4dEbGTiseJW5tXzu","content":[{"type":"tool_reference","tool_name":"WebSearch"},{"type":"tool_reference","tool_name":"WebFetch"}]}]},"uuid":"5b55119d-82fe-43de-9ea1-5ca80686f7f6","timestamp":"2026-03-20T19:06:50.785Z","sourceToolAssistantUUID":"1c5d3101-b614-4046-940c-2c86949656f2","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"5b55119d-82fe-43de-9ea1-5ca80686f7f6","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"text","text":"\n\nNow let me search for key events across the consolidate stack. I'll run multiple searches in parallel."}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"cache_creation":{"ephemeral_5m_input_tokens":1148,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"6385efbc-8643-4ff3-9598-ea8eac703834","timestamp":"2026-03-20T19:06:54.440Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"6385efbc-8643-4ff3-9598-ea8eac703834","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_012cP5Pp2KSH6BVouFe3STjC","name":"WebSearch","input":{"query":"Capricor Therapeutics HOPE-2 trial results DMD deramiocel CAP-1002"},"caller":{"type":"direct"}}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"cache_creation":{"ephemeral_5m_input_tokens":1148,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"351063f1-9870-4936-b3e4-53b6ac76af92","timestamp":"2026-03-20T19:06:55.368Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"351063f1-9870-4936-b3e4-53b6ac76af92","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_01TGwpKvEZcZc3GYdeDHxTCQ","name":"WebSearch","input":{"query":"Capricor Therapeutics earnings call 2024 2025 deramiocel results"},"caller":{"type":"direct"}}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"cache_creation":{"ephemeral_5m_input_tokens":1148,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"5a2eff98-02be-4b54-8fd9-84b13e5ecf9a","timestamp":"2026-03-20T19:06:56.064Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"5a2eff98-02be-4b54-8fd9-84b13e5ecf9a","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"query_update","query":"Capricor Therapeutics HOPE-2 trial results DMD deramiocel CAP-1002"},"toolUseID":"search-progress-1","parentToolUseID":"toolu_012cP5Pp2KSH6BVouFe3STjC","uuid":"1f1d6dfe-fec5-4166-a85c-469141a1d900","timestamp":"2026-03-20T19:06:56.088Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"1f1d6dfe-fec5-4166-a85c-469141a1d900","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_01RMKHNrHDLECm6TUh593mtU","name":"WebSearch","input":{"query":"Capricor Therapeutics Nippon Shinyaku partnership deramiocel"},"caller":{"type":"direct"}}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"cache_creation":{"ephemeral_5m_input_tokens":1148,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"f060edf1-e960-4efe-846a-23bcdce02a0d","timestamp":"2026-03-20T19:06:56.670Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"f060edf1-e960-4efe-846a-23bcdce02a0d","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"query_update","query":"Capricor Therapeutics earnings call 2024 2025 deramiocel results"},"toolUseID":"search-progress-1","parentToolUseID":"toolu_01TGwpKvEZcZc3GYdeDHxTCQ","uuid":"6503d187-98d1-4dcd-ac50-704aace29c2a","timestamp":"2026-03-20T19:06:56.731Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"6503d187-98d1-4dcd-ac50-704aace29c2a","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"search_results_received","resultCount":10,"query":"Capricor Therapeutics HOPE-2 trial results DMD deramiocel CAP-1002"},"toolUseID":"srvtoolu_01NdRX1tz3atWhPn2vf5UfvB","parentToolUseID":"toolu_012cP5Pp2KSH6BVouFe3STjC","uuid":"b528a666-e9cc-48f4-8ea6-c2b4fe4ad2b6","timestamp":"2026-03-20T19:06:57.298Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"b528a666-e9cc-48f4-8ea6-c2b4fe4ad2b6","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"query_update","query":"Capricor Therapeutics Nippon Shinyaku partnership deramiocel"},"toolUseID":"search-progress-1","parentToolUseID":"toolu_01RMKHNrHDLECm6TUh593mtU","uuid":"318933eb-d30d-466d-804b-638ed941cc31","timestamp":"2026-03-20T19:06:57.320Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"318933eb-d30d-466d-804b-638ed941cc31","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_01DuRuh4tiUcEFXBZ3mabwQP","name":"WebSearch","input":{"query":"Capricor Therapeutics Michael Binks CMO hire 2025"},"caller":{"type":"direct"}}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"cache_creation":{"ephemeral_5m_input_tokens":1148,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"b85ced7c-2171-468b-a885-fcf2994003bd","timestamp":"2026-03-20T19:06:57.708Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"b85ced7c-2171-468b-a885-fcf2994003bd","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_016h3t3XaqpycwUkJbjK7Zd8","name":"WebSearch","input":{"query":"Capricor Therapeutics Shkreli short report CAPR 2025"},"caller":{"type":"direct"}}],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"cache_creation":{"ephemeral_5m_input_tokens":1148,"ephemeral_1h_input_tokens":0},"output_tokens":2,"service_tier":"standard","inference_geo":"not_available"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"7c8f6671-eeb4-48ec-a9f2-31e4b964049b","timestamp":"2026-03-20T19:06:58.246Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"7c8f6671-eeb4-48ec-a9f2-31e4b964049b","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"search_results_received","resultCount":10,"query":"Capricor Therapeutics earnings call 2024 2025 deramiocel results"},"toolUseID":"srvtoolu_01FBiV1nCXbFgEx84SgdMrX1","parentToolUseID":"toolu_01TGwpKvEZcZc3GYdeDHxTCQ","uuid":"28272aa0-8664-4589-b4e7-15ebc40db8e7","timestamp":"2026-03-20T19:06:58.349Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"28272aa0-8664-4589-b4e7-15ebc40db8e7","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"query_update","query":"Capricor Therapeutics Michael Binks CMO hire 2025"},"toolUseID":"search-progress-1","parentToolUseID":"toolu_01DuRuh4tiUcEFXBZ3mabwQP","uuid":"79982781-f3cc-4e5b-9ed8-8c64e20cea70","timestamp":"2026-03-20T19:06:58.497Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"79982781-f3cc-4e5b-9ed8-8c64e20cea70","isSidechain":true,"agentId":"a518bc4e78426ebc2","message":{"model":"claude-opus-4-6","id":"msg_01U2W2GxuskKXSx22i4Y8h4b","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_01E6URJ19Yk9zm7Lto8czbLw","name":"WebSearch","input":{"query":"Capricor Therapeutics securities fraud class action lawsuit 2025"},"caller":{"type":"direct"}}],"stop_reason":"tool_use","stop_sequence":null,"usage":{"input_tokens":3,"cache_creation_input_tokens":1148,"cache_read_input_tokens":11157,"output_tokens":360,"server_tool_use":{"web_search_requests":0,"web_fetch_requests":0},"service_tier":"standard","cache_creation":{"ephemeral_1h_input_tokens":0,"ephemeral_5m_input_tokens":1148},"inference_geo":"","iterations":[],"speed":"standard"}},"requestId":"req_011CZErbv292PkncmPqBNhS8","type":"assistant","uuid":"1e8c30ed-774f-4b7b-afea-4bab0a9e4b0d","timestamp":"2026-03-20T19:06:58.499Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"1e8c30ed-774f-4b7b-afea-4bab0a9e4b0d","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"search_results_received","resultCount":10,"query":"Capricor Therapeutics Nippon Shinyaku partnership deramiocel"},"toolUseID":"srvtoolu_01V4sH6UUTV7ZCnn8jKchcBV","parentToolUseID":"toolu_01RMKHNrHDLECm6TUh593mtU","uuid":"642c6fec-6082-46e9-afd0-564939b20940","timestamp":"2026-03-20T19:06:58.766Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"642c6fec-6082-46e9-afd0-564939b20940","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"query_update","query":"Capricor Therapeutics Shkreli short report CAPR 2025"},"toolUseID":"search-progress-1","parentToolUseID":"toolu_016h3t3XaqpycwUkJbjK7Zd8","uuid":"75c51df3-ef83-496b-b895-49029953dd71","timestamp":"2026-03-20T19:06:59.022Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
{"parentUuid":"75c51df3-ef83-496b-b895-49029953dd71","isSidechain":true,"agentId":"a518bc4e78426ebc2","type":"progress","data":{"type":"query_update","query":"Capricor Therapeutics securities fraud class action lawsuit 2025"},"toolUseID":"search-progress-1","parentToolUseID":"toolu_01E6URJ19Yk9zm7Lto8czbLw","uuid":"e5082902-ab62-4dfd-a902-b0d79e4e4590","timestamp":"2026-03-20T19:06:59.224Z","userType":"external","entrypoint":"cli","cwd":"/Users/junekim/Documents/june.kim","sessionId":"6d5431e1-97f0-46be-9bdf-36e96721569f","version":"2.1.79","gitBranch":"master","slug":"modular-sparking-forest"}
codex
I have the merged chronology and the disagreement point. I’m checking the preregistered CAPR catalyst fields now so the prediction record uses the exact window and pass condition rather than paraphrasing them.
exec
/bin/zsh -lc "sed -n '249,265p' prereg.md" in /Users/junekim/Documents/universal-diagnosis succeeded in 0ms:
## Appendix: Run 0 catalyst definitions (demonstration — retrospective, outcome known)

### CAPR (Capricor Therapeutics)
- **Catalyst**: HOPE-3 Phase 3 topline readout for Deramiocel in DMD
- **Source**: Capricor Therapeutics press release (capricor.com) or SEC 8-K
- **Window**: 2025-10-01 to 2025-12-31 (outcome known: Dec 3, 2025)
- **PASS condition**: Primary endpoint (PUL v2.0 total score) statistically significant
- **Outcome**: PASS (p=0.029 primary, p=0.041 LVEF key secondary). Known.
- **Shkreli position**: Bear (short, 46-page report, "it will not work", Nov 24 2025)

### QURE (uniQure)
- **Catalyst**: AMT-130 Phase I/II topline readout for Huntington's disease (36-month data)
- **Source**: uniQure press release via uniqure.com or SEC 8-K
- **Window**: 2025-08-01 to 2025-10-31 (outcome known: Sep 2025)
- **PASS condition**: Primary endpoint (cUHDRS) statistically significant vs. external control
- **Outcome**: PASS (75% slowing, p significant). Known. But: FDA subsequently said data not sufficient for marketing application (Jan 2026 Type A meeting). Company now seeking Type B meeting for Phase III design.
- **Shkreli position**: Bull (long, saw 5-10x, sold Nov 2025 — before FDA pushback)
codex
**S**  
Capricor framed deramiocel as a learnable DMD program that had moved beyond the failed cardiology/ALLSTAR era: management highlighted the DMD pivot, RMAT support, HOPE-2/OLE durability, a 2024-2025 BLA strategy based on HOPE-2 plus natural history, and then an immediate resubmission path after the July 11, 2025 CRL using HOPE-3 data. Martin Shkreli publicly shorted CAPR on November 24, 2025 and argued HOPE-3 “will not work,” effectively treating the company as a bad snapshot; HOPE-3 then succeeded on December 3, 2025 and his short was wrong. Under this framework, the company is the consolidate stack, and the key question is whether it learned fast enough to rebuild the path from failure to controlled Phase 3 success.

**O**

| Date | Pipe | Status | Evidence |
|---|---|---|---|
| 2012-02-14 | perceive_cache | functional | CADUCEUS supported myocardial delivery/activity. |
| 2017-05-12 | read_outcomes | broken | ALLSTAR futility on scar-reduction primary endpoint. |
| 2017-05-12 | batch_process | functional | Same-day pivot announcement toward DMD. |
| 2017-07-07 | write_substrate | functional | Janssen exits; Capricor retains rights and fully pivots. |
| 2018-01-23 | write_substrate | functional | HOPE-2 redesign posted: IV route, multi-dose, randomized, double-blind. |
| 2018-02-05 | batch_process | functional | FDA grants RMAT. |
| 2019-01-22 | read_outcomes | functional | FDA RMAT meeting supports PUL-based path and further interaction. |
| 2020-09-21 | filter_attend | broken | ALLSTAR publication confirms wrong readout/no efficacy signal. |
| 2022-03-12 | filter_attend | repaired | HOPE-2 captures DMD signal with revised endpoint; p=0.014. |
| 2024-08-07 | batch_process | functional | Pre-BLA meeting positive; company chooses HOPE-2/OLE + natural history filing strategy. |
| 2024-09-24 | write_substrate | functional | BLA decision made without waiting for HOPE-3. |
| 2025-03-04 | batch_process | functional | BLA accepted; Priority Review granted. |
| 2025-05-13 | batch_process | stressed | Mid-cycle review says no major deficiencies, but AdCom planning signals risk. |
| 2025-07-11 | read_outcomes | broken | CRL: application lacks substantial evidence of effectiveness. |
| 2025-07-11 | batch_process | functional | Same-day decision to use HOPE-3 for resubmission path. |
| 2025-08-11 | write_substrate | repaired | Type A meeting, 483 issues resolved, protocol/regulatory package adjusted. |
| 2025-11-10 | batch_process | repaired | FDA supports HOPE-3 as the additional study needed. |
| 2025-11-24 | read_outcomes | stressed | Shkreli short report challenges management narrative and predicts failure. |
| 2025-12-03 | read_outcomes | repaired | HOPE-3 topline positive: PUL v2.0 p=0.029, LVEF p=0.041. |
| 2025-12-05 | write_substrate | functional | $150M financing supports launch/commercialization prep. |
| 2026-03-10 | write_substrate | repaired | FDA resumes review; new PDUFA set for August 22, 2026. |

Transitions:
- `filter_attend`: broken on September 21, 2020 -> repaired on March 12, 2022. The forward pass found a better endpoint/readout.
- `read_outcomes`: broken on July 11, 2025 -> repaired on December 3, 2025. The evidentiary gap exposed by the CRL was closed by HOPE-3.
- `write_substrate`: stressed/broken regulatory package in mid-2025 -> repaired by August 11, 2025 and March 10, 2026 through protocol, CMC, and resubmission changes.
- `batch_process`: stressed on May 13, 2025 -> repaired by November 10, 2025 when the company aligned its strategy to FDA’s actual requirement.

**A**  
Diagnosis: the decisive change was driven by the consolidate stack, not by a static forward-pass snapshot. Capricor read the ALLSTAR failure, pivoted indication, rewrote route/design/endpoints in HOPE-2/HOPE-3, then after the July 11, 2025 CRL processed the failure quickly enough to preserve the program and convert HOPE-3 into the needed controlled evidence. Trajectory category: `dying_pivoted`. The program looked dying in its original cardiology form and again at the July 2025 CRL, but the company pivoted and repaired rather than repeating the same path. Trauma recurrence is disputed: Consolidate-A says `no` because ALLSTAR was a scientific/indication failure while the CRL was a regulatory/evidence-packaging failure; Consolidate-B says `yes` because the CRL and later securities-fraud allegations both reflect the same management-readout gap between public confidence and FDA’s actual evidentiary view. On balance, the merged diagnosis is that recurrence at the level of exact failure class is unproven, but recurrence of overconfident interpretation is a live concern.

**P**

| Field | Value |
|---|---|
| Company | Capricor Therapeutics (`CAPR`) |
| Type | Run 0 retrospective prediction |
| Category | `dying_pivoted` |
| Direction | `PASS` |
| Catalyst | HOPE-3 Phase 3 topline readout for deramiocel in DMD |
| Resolution source | Capricor press release or SEC 8-K announcing HOPE-3 topline |
| Window start | 2025-10-01 |
| Window end | 2025-12-31 |
| Pass condition | Primary endpoint, PUL v2.0 total score, statistically significant |
| Reasoning | The company is the consolidate stack, and its trajectory showed real learning: post-ALLSTAR indication pivot, route and trial redesign, endpoint repair, preserved durability/safety signal, and after the July 11, 2025 CRL an immediate switch to the already-running HOPE-3 controlled dataset. Shkreli shorted a snapshot in late November 2025; the framework would have predicted the repaired trajectory to resolve as PASS. |

**Refs**  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420417026609/v466873_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420417026609/v466873_ex99-1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420417035956/v470439_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420417035956/v470439_ex99-1.htm)  
[https://clinicaltrials.gov/study/NCT03406780](https://clinicaltrials.gov/study/NCT03406780)  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420418005594/tv484839_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420418005594/tv484839_ex99-1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420419002173/tv511315_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420419002173/tv511315_ex99-1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837024011350/capr-20240807xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837024011350/capr-20240807xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837024012983/capr-20240924xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837024012983/capr-20240924xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837024013207/capr-20241009xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837024013207/capr-20241009xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025000010/capr-20250102xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025000010/capr-20250102xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025002097/capr-20250304xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025002097/capr-20250304xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025007574/capr-20250513xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025007574/capr-20250513xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/315/capricor-therapeutics-announces-key-regulatory-updates-for](https://www.capricor.com/investors/news-events/press-releases/detail/315/capricor-therapeutics-announces-key-regulatory-updates-for)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025009186/capr-20250711xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025009186/capr-20250711xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/319/capricor-therapeutics-provides-regulatory-update-on](https://www.capricor.com/investors/news-events/press-releases/detail/319/capricor-therapeutics-provides-regulatory-update-on)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025011047/capr-20250811xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025011047/capr-20250811xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/326/capricor-therapeutics-provides-regulatory-update-on](https://www.capricor.com/investors/news-events/press-releases/detail/326/capricor-therapeutics-provides-regulatory-update-on)  
[https://www.benzinga.com/trading-ideas/movers/25/11/49040350/martin-shkreli-takes-aim-at-capricor-stock-sinks](https://www.benzinga.com/trading-ideas/movers/25/11/49040350/martin-shkreli-takes-aim-at-capricor-stock-sinks)  
[https://www.capricor.com/investors/news-events/press-releases/detail/331/capricor-therapeutics-announces-positive-topline-results](https://www.capricor.com/investors/news-events/press-releases/detail/331/capricor-therapeutics-announces-positive-topline-results)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465925117947/capr-20251203xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465925117947/capr-20251203xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465925118934/capr-20251205xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465925118934/capr-20251205xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465926025657/capr-20260310xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465926025657/capr-20260310xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/338/capricor-therapeutics-announces-establishment-of-new-pdufa](https://www.capricor.com/investors/news-events/press-releases/detail/338/capricor-therapeutics-announces-establishment-of-new-pdufa)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465926027037/capr-20260312xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465926027037/capr-20260312xex99d1.htm)  
[https://www.globenewswire.com/news-release/2025/07/21/3119053/0/en/Capricor-Therapeutics-Inc-Securities-Fraud-Class-Action-Lawsuit-Pending-Contact-The-Gross-Law-Firm-Before-September-15-2025-to-Discuss-Your-Rights-CAPR.html](https://www.globenewswire.com/news-release/2025/07/21/3119053/0/en/Capricor-Therapeutics-Inc-Securities-Fraud-Class-Action-Lawsuit-Pending-Contact-The-Gross-Law-Firm-Before-September-15-2025-to-Discuss-Your-Rights-CAPR.html)
tokens used
37,898
**S**  
Capricor framed deramiocel as a learnable DMD program that had moved beyond the failed cardiology/ALLSTAR era: management highlighted the DMD pivot, RMAT support, HOPE-2/OLE durability, a 2024-2025 BLA strategy based on HOPE-2 plus natural history, and then an immediate resubmission path after the July 11, 2025 CRL using HOPE-3 data. Martin Shkreli publicly shorted CAPR on November 24, 2025 and argued HOPE-3 “will not work,” effectively treating the company as a bad snapshot; HOPE-3 then succeeded on December 3, 2025 and his short was wrong. Under this framework, the company is the consolidate stack, and the key question is whether it learned fast enough to rebuild the path from failure to controlled Phase 3 success.

**O**

| Date | Pipe | Status | Evidence |
|---|---|---|---|
| 2012-02-14 | perceive_cache | functional | CADUCEUS supported myocardial delivery/activity. |
| 2017-05-12 | read_outcomes | broken | ALLSTAR futility on scar-reduction primary endpoint. |
| 2017-05-12 | batch_process | functional | Same-day pivot announcement toward DMD. |
| 2017-07-07 | write_substrate | functional | Janssen exits; Capricor retains rights and fully pivots. |
| 2018-01-23 | write_substrate | functional | HOPE-2 redesign posted: IV route, multi-dose, randomized, double-blind. |
| 2018-02-05 | batch_process | functional | FDA grants RMAT. |
| 2019-01-22 | read_outcomes | functional | FDA RMAT meeting supports PUL-based path and further interaction. |
| 2020-09-21 | filter_attend | broken | ALLSTAR publication confirms wrong readout/no efficacy signal. |
| 2022-03-12 | filter_attend | repaired | HOPE-2 captures DMD signal with revised endpoint; p=0.014. |
| 2024-08-07 | batch_process | functional | Pre-BLA meeting positive; company chooses HOPE-2/OLE + natural history filing strategy. |
| 2024-09-24 | write_substrate | functional | BLA decision made without waiting for HOPE-3. |
| 2025-03-04 | batch_process | functional | BLA accepted; Priority Review granted. |
| 2025-05-13 | batch_process | stressed | Mid-cycle review says no major deficiencies, but AdCom planning signals risk. |
| 2025-07-11 | read_outcomes | broken | CRL: application lacks substantial evidence of effectiveness. |
| 2025-07-11 | batch_process | functional | Same-day decision to use HOPE-3 for resubmission path. |
| 2025-08-11 | write_substrate | repaired | Type A meeting, 483 issues resolved, protocol/regulatory package adjusted. |
| 2025-11-10 | batch_process | repaired | FDA supports HOPE-3 as the additional study needed. |
| 2025-11-24 | read_outcomes | stressed | Shkreli short report challenges management narrative and predicts failure. |
| 2025-12-03 | read_outcomes | repaired | HOPE-3 topline positive: PUL v2.0 p=0.029, LVEF p=0.041. |
| 2025-12-05 | write_substrate | functional | $150M financing supports launch/commercialization prep. |
| 2026-03-10 | write_substrate | repaired | FDA resumes review; new PDUFA set for August 22, 2026. |

Transitions:
- `filter_attend`: broken on September 21, 2020 -> repaired on March 12, 2022. The forward pass found a better endpoint/readout.
- `read_outcomes`: broken on July 11, 2025 -> repaired on December 3, 2025. The evidentiary gap exposed by the CRL was closed by HOPE-3.
- `write_substrate`: stressed/broken regulatory package in mid-2025 -> repaired by August 11, 2025 and March 10, 2026 through protocol, CMC, and resubmission changes.
- `batch_process`: stressed on May 13, 2025 -> repaired by November 10, 2025 when the company aligned its strategy to FDA’s actual requirement.

**A**  
Diagnosis: the decisive change was driven by the consolidate stack, not by a static forward-pass snapshot. Capricor read the ALLSTAR failure, pivoted indication, rewrote route/design/endpoints in HOPE-2/HOPE-3, then after the July 11, 2025 CRL processed the failure quickly enough to preserve the program and convert HOPE-3 into the needed controlled evidence. Trajectory category: `dying_pivoted`. The program looked dying in its original cardiology form and again at the July 2025 CRL, but the company pivoted and repaired rather than repeating the same path. Trauma recurrence is disputed: Consolidate-A says `no` because ALLSTAR was a scientific/indication failure while the CRL was a regulatory/evidence-packaging failure; Consolidate-B says `yes` because the CRL and later securities-fraud allegations both reflect the same management-readout gap between public confidence and FDA’s actual evidentiary view. On balance, the merged diagnosis is that recurrence at the level of exact failure class is unproven, but recurrence of overconfident interpretation is a live concern.

**P**

| Field | Value |
|---|---|
| Company | Capricor Therapeutics (`CAPR`) |
| Type | Run 0 retrospective prediction |
| Category | `dying_pivoted` |
| Direction | `PASS` |
| Catalyst | HOPE-3 Phase 3 topline readout for deramiocel in DMD |
| Resolution source | Capricor press release or SEC 8-K announcing HOPE-3 topline |
| Window start | 2025-10-01 |
| Window end | 2025-12-31 |
| Pass condition | Primary endpoint, PUL v2.0 total score, statistically significant |
| Reasoning | The company is the consolidate stack, and its trajectory showed real learning: post-ALLSTAR indication pivot, route and trial redesign, endpoint repair, preserved durability/safety signal, and after the July 11, 2025 CRL an immediate switch to the already-running HOPE-3 controlled dataset. Shkreli shorted a snapshot in late November 2025; the framework would have predicted the repaired trajectory to resolve as PASS. |

**Refs**  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420417026609/v466873_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420417026609/v466873_ex99-1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420417035956/v470439_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420417035956/v470439_ex99-1.htm)  
[https://clinicaltrials.gov/study/NCT03406780](https://clinicaltrials.gov/study/NCT03406780)  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420418005594/tv484839_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420418005594/tv484839_ex99-1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000114420419002173/tv511315_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000114420419002173/tv511315_ex99-1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837024011350/capr-20240807xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837024011350/capr-20240807xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837024012983/capr-20240924xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837024012983/capr-20240924xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837024013207/capr-20241009xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837024013207/capr-20241009xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025000010/capr-20250102xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025000010/capr-20250102xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025002097/capr-20250304xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025002097/capr-20250304xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025007574/capr-20250513xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025007574/capr-20250513xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/315/capricor-therapeutics-announces-key-regulatory-updates-for](https://www.capricor.com/investors/news-events/press-releases/detail/315/capricor-therapeutics-announces-key-regulatory-updates-for)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025009186/capr-20250711xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025009186/capr-20250711xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/319/capricor-therapeutics-provides-regulatory-update-on](https://www.capricor.com/investors/news-events/press-releases/detail/319/capricor-therapeutics-provides-regulatory-update-on)  
[https://www.sec.gov/Archives/edgar/data/1133869/000155837025011047/capr-20250811xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000155837025011047/capr-20250811xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/326/capricor-therapeutics-provides-regulatory-update-on](https://www.capricor.com/investors/news-events/press-releases/detail/326/capricor-therapeutics-provides-regulatory-update-on)  
[https://www.benzinga.com/trading-ideas/movers/25/11/49040350/martin-shkreli-takes-aim-at-capricor-stock-sinks](https://www.benzinga.com/trading-ideas/movers/25/11/49040350/martin-shkreli-takes-aim-at-capricor-stock-sinks)  
[https://www.capricor.com/investors/news-events/press-releases/detail/331/capricor-therapeutics-announces-positive-topline-results](https://www.capricor.com/investors/news-events/press-releases/detail/331/capricor-therapeutics-announces-positive-topline-results)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465925117947/capr-20251203xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465925117947/capr-20251203xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465925118934/capr-20251205xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465925118934/capr-20251205xex99d1.htm)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465926025657/capr-20260310xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465926025657/capr-20260310xex99d1.htm)  
[https://www.capricor.com/investors/news-events/press-releases/detail/338/capricor-therapeutics-announces-establishment-of-new-pdufa](https://www.capricor.com/investors/news-events/press-releases/detail/338/capricor-therapeutics-announces-establishment-of-new-pdufa)  
[https://www.sec.gov/Archives/edgar/data/1133869/000110465926027037/capr-20260312xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1133869/000110465926027037/capr-20260312xex99d1.htm)  
[https://www.globenewswire.com/news-release/2025/07/21/3119053/0/en/Capricor-Therapeutics-Inc-Securities-Fraud-Class-Action-Lawsuit-Pending-Contact-The-Gross-Law-Firm-Before-September-15-2025-to-Discuss-Your-Rights-CAPR.html](https://www.globenewswire.com/news-release/2025/07/21/3119053/0/en/Capricor-Therapeutics-Inc-Securities-Fraud-Class-Action-Lawsuit-Pending-Contact-The-Gross-Law-Firm-Before-September-15-2025-to-Discuss-Your-Rights-CAPR.html)
