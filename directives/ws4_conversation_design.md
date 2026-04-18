# Directive: WS-4 Conversation Design & Knowledge Setup

**Workstream:** WS-4  
**Owner:** Ajaia AI/Conversation Designer + Client Clinical Ops  
**Timeline:** Weeks 3–4  
**Dependency:** WS-1 sign-off (scope and patient journey must be defined)

---

## Goal

Design the agent's conversation flows for every patient-facing scenario, populate the knowledge base with clinic-specific information, and define escalation paths so no patient conversation ends in silence.

---

## Inputs Required

| Input | Source | Required By |
|---|---|---|
| Agreed agent scope (channels, use cases) | WS-1 output | Before design starts |
| Patient journey map | WS-1 output | Before design starts |
| FAQ document (services, insurance, clinic hours, prep instructions) | Client Clinical Ops | Week 3 |
| List of appointment types and associated questions patients typically ask | Client Clinical Ops | Week 3 |
| Escalation routing rules (what triggers a handoff, to whom) | Client Ops + Clinical | Week 3 |
| Tone and brand guidelines | Client Marketing/Ops | Week 3 |

---

## Steps

1. **Conversation flow mapping** — Design flows for: inbound new inquiry, dormant lead re-engagement, scheduling conversation, confirmation/reminder, and escalation. Use flowchart format.
2. **Knowledge base population** — Translate client FAQs, service descriptions, insurance info, and prep instructions into structured KB entries the agent can retrieve.
3. **Guardrail definition** — Define explicit no-go zones: clinical advice, diagnosis, medication questions. Agent must redirect these to clinical staff immediately.
4. **Escalation playbook** — Define every trigger that routes to a human: keywords (e.g., "urgent", "emergency"), unrecognized intent, patient frustration signals, 3 failed clarification attempts.
5. **Prompt/instruction set draft** — Write the system prompt and instruction set for the AI agent. Include persona, scope constraints, escalation rules, and tone guidance.
6. **Client review session** — Walk through all flows and sample conversations with client clinical ops. Get written sign-off before moving to WS-5.

---

## Outputs

- [ ] Conversation flow diagrams (all scenarios: inbound, dormant, scheduling, confirmation, escalation)
- [ ] Agent knowledge base (FAQs, clinic info, appointment prep)
- [ ] Escalation + fallback playbook
- [ ] Guardrail definitions (clinical no-go zones)
- [ ] System prompt and instruction set (v1, client-approved)
- [ ] 10+ sample conversations reviewed and signed off by client

---

## Edge Cases & Flags

- **Client FAQs are incomplete or outdated** → Do not populate KB with unverified content. Identify gaps and schedule a 1-hour content session with clinical ops.
- **Escalation routing unclear** → Default to "human review required" for any ambiguous case. Never let the agent guess at routing.
- **Agent produces hallucinated clinic info in testing** → Reduce KB reliance on free-form generation. Switch to retrieval-only for factual fields (hours, insurance, address).
- **Client wants the agent to answer clinical questions** → Hard no. Document the boundary clearly, get sign-off, and add it to compliance record.
- **Multiple languages needed** → Flag early. Multilingual support doubles QA scope. Descope to English-only for pilot unless client has a hard requirement.

---

## Execution Tools

- `execution/launch_readiness_tracker.py` — conversation design items tracked as readiness criteria

---

## Learnings Log

> Update this section as the engagement progresses.

- *(none yet — engagement not started)*
