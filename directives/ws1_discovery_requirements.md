# Directive: WS-1 Discovery & Requirements Alignment

**Workstream:** WS-1  
**Owner:** AI Solutions Architect (Ajaia) + Client Operations Lead  
**Timeline:** Weeks 1–2  
**Status:** Active at engagement start

---

## Goal

Understand the client's current patient acquisition workflow end-to-end, define the agent's scope, and produce a signed-off requirements document before any build begins.

---

## Inputs Required

| Input | Source | Required By |
|---|---|---|
| Stakeholder list (ops, IT, compliance, clinical scheduling) | Client DRI | Day 1 |
| Current CRM/EHR workflow documentation | Client IT | Day 3 |
| List of appointment types and provider categories in scope | Client Clinical Ops | Day 3 |
| Sample lead records (anonymized) | Client CRM admin | Day 5 |
| Current response time and conversion rate baselines | Client Ops | Week 2 |

---

## Steps

1. **Kickoff session** — Align stakeholders on engagement goals, timeline, and decision-making authority. Identify single client DRI.
2. **Process shadowing** — Walk through the current patient inquiry-to-appointment workflow step by step. Map every handoff point.
3. **Scope definition workshop** — Agree on: which channels (SMS/email/chat), which lead types (inbound vs. dormant), which appointment categories, escalation triggers.
4. **Data dictionary draft** — Enumerate every data field the agent will read or write: lead status, contact fields, appointment type, provider ID, availability format.
5. **Success metrics baseline** — Capture current state: conversion rate from inquiry to booked, average response time, open slot fill rate.
6. **Requirements doc draft + review** — Write, circulate, and get sign-off from client ops and IT.

---

## Outputs

- [ ] Current-state workflow map (patient journey: inquiry → scheduled appointment)
- [ ] Agent scope document (channels, use cases, escalation rules)
- [ ] Success metrics baseline (pre-AI benchmarks)
- [ ] Signed requirements document
- [ ] Preliminary data dictionary

---

## Edge Cases & Flags

- **Multiple stakeholders disagree on scope** → Escalate to DRI within 24 hours. Do not proceed with contested scope.
- **No baseline metrics available** → Agree on proxy metrics for the pilot period. Document the gap.
- **Appointment types are highly varied** → Narrow scope to top 2 by volume for pilot. Expand post-validation.
- **Client doesn't have a single DRI** → Block discovery sign-off until one is assigned. Raise as RISK-05.

---

## Execution Tools

- `execution/generate_status_update.py` — auto-generate weekly status update from workstream data
- `execution/launch_readiness_tracker.py` — track open items and completion state

---

## Learnings Log

> Update this section as the engagement progresses. Document API constraints, timing surprises, or edge cases encountered.

- *(none yet — engagement not started)*
