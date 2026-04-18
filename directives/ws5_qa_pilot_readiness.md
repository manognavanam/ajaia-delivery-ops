# Directive: WS-5 QA & Pilot Readiness

**Workstream:** WS-5  
**Owner:** Ajaia QA Lead + Client Operations Lead  
**Timeline:** Weeks 5–6  
**Dependency:** WS-3 integrations in staging + WS-4 conversation flows finalized

---

## Goal

Validate the agent end-to-end in a staging environment before any live patient exposure. Produce a binary go/no-go decision backed by a completed launch criteria checklist.

---

## Inputs Required

| Input | Source | Required By |
|---|---|---|
| Staging environment with integrations live | WS-3 output | Start of Week 5 |
| Finalized conversation flows and system prompt | WS-4 output | Start of Week 5 |
| Test lead dataset (synthetic or anonymized — no real PHI) | Ajaia QA + Client | Week 5 |
| Defined pass/fail criteria for each test scenario | WS-3 + WS-4 leads | Week 5 |
| Escalation path contacts (who receives escalated conversations in staging) | Client Ops | Week 5 |

---

## Steps

1. **Test plan creation** — Define test scenarios: happy path, edge cases, escalation triggers, integration failure modes, PHI handling.
2. **Integration testing** — Verify: CRM sync works, calendar writes correctly, outreach delivers, opt-out is respected.
3. **Conversation testing** — Run scripted test conversations for all flows. Include adversarial inputs (clinical questions, gibberish, angry patient language).
4. **Escalation path verification** — Trigger every escalation scenario. Confirm handoff reaches the right person via the right channel.
5. **Load and latency check** — Simulate concurrent conversations. Confirm near-real-time response for chat/SMS interactions.
6. **Launch criteria review** — Score every item on the launch criteria checklist. Any red item = no-go.

---

## Outputs

- [ ] QA test plan (scenarios, inputs, expected outputs, pass/fail)
- [ ] QA test results document
- [ ] Escalation path verification sign-off
- [ ] Known issues log with severity and resolution status
- [ ] Launch criteria checklist (all items green = go)
- [ ] Staging environment sign-off memo

---

## Launch Criteria Checklist (Go/No-Go Gates)

| Criteria | Owner | Status |
|---|---|---|
| All integration tests pass in staging | Ajaia Eng | — |
| No PHI leaves approved data boundaries | Ajaia Compliance | — |
| All conversation flows tested end-to-end | Ajaia QA | — |
| Every escalation trigger routes correctly | Ajaia QA + Client Ops | — |
| Opt-out mechanism tested and confirmed | Ajaia Eng | — |
| Latency < 5 seconds for chat/SMS response | Ajaia Eng | — |
| Client ops staff trained on receiving escalations | Client Ops | — |
| Rollback plan documented and tested | Ajaia Eng | — |
| Client sign-off on sample conversation quality | Client Clinical Ops | — |

---

## Edge Cases & Flags

- **Integration passes unit tests but fails end-to-end** → Re-open WS-3. Do not compress QA time to compensate for integration delays.
- **Agent gives incorrect clinic information in testing** → Freeze pilot. Return to WS-4 to fix KB before any live exposure.
- **Escalation handoff delivers to wrong person** → Block go-live. Routing errors in a healthcare context are a patient safety issue.
- **Load testing reveals latency spikes** → Investigate async handling, caching, and API rate limit buffering before pilot.

---

## Execution Tools

- `execution/launch_readiness_tracker.py` — the primary tool for this workstream; tracks every launch criteria item

---

## Learnings Log

> Update this section as the engagement progresses.

- *(none yet — engagement not started)*
