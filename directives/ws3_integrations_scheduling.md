# Directive: WS-3 Integrations & Scheduling Systems

**Workstream:** WS-3  
**Owner:** Ajaia Engineering Lead + Client IT  
**Timeline:** Weeks 3–5  
**Dependency:** WS-1 sign-off + WS-2 compliance gate (HARD BLOCK)

---

## Goal

Connect the AI agent to the client's CRM (lead data), EHR/scheduling system (provider calendars), and outreach channels (SMS/email). All connections must be tested in staging before WS-5 begins.

---

## Inputs Required

| Input | Source | Required By |
|---|---|---|
| CRM API documentation and sandbox credentials | Client IT | Start of Week 3 |
| EHR scheduling API documentation (Epic FHIR, Athena, etc.) | Client IT | Start of Week 3 |
| Appointment booking rules (slot durations, buffer times, provider preferences) | Client Clinical Ops | Week 3 |
| Outreach channel credentials (Twilio account, email provider) | Ajaia Eng | Week 3 |
| PHI-approved data fields list (from WS-2) | WS-2 output | Before build starts |
| Staging/test environment access | Client IT | Day 1 of WS-3 |

---

## Steps

1. **IT kickoff** — Separate session with client IT (not the business kickoff). Confirm API access, auth method (OAuth/API key), sandbox availability, and rate limits.
2. **CRM integration** — Build lead ingestion: pull active and dormant leads, map to agent's data model, write status updates back after outreach.
3. **Calendar/scheduling integration** — Read provider availability, write confirmed appointments. Test with at least 2 provider calendars and 2 appointment types.
4. **Outreach channel setup** — Configure SMS (Twilio or equivalent) and email. Set up opt-out handling at channel level.
5. **Data mapping specification** — Document every field transformation between source system and agent layer.
6. **End-to-end staging test** — Full flow: lead pulled from CRM → agent engages → slot booked → confirmation sent → status written back to CRM.

---

## Outputs

- [ ] CRM ↔ Agent sync (lead ingestion + status write-back)
- [ ] Calendar API integration (read availability + write appointments)
- [ ] Outreach channel setup (SMS + email, with opt-out)
- [ ] Data mapping specification document
- [ ] Integration test results (pass/fail per scenario)
- [ ] Staging environment sign-off

---

## Technical Readiness Criteria ("Ready to Build" Definition)

Before a single line of integration code is written, all of the following must be true:

- [ ] Sandbox credentials delivered and validated (can authenticate successfully)
- [ ] API rate limits documented (know how many calls/min are allowed)
- [ ] Appointment booking rules written down and signed off by clinical ops
- [ ] PHI fields classified and approved by compliance (WS-2 gate cleared)
- [ ] Rollback plan defined (if integration breaks in staging, how do we recover)

---

## What Could Go Wrong

| Risk | Signal | Response |
|---|---|---|
| EHR API access delayed by IT procurement | No credentials by Week 3 Day 3 | Escalate to DRI; build CRM integration first; use CSV export as temporary fallback |
| EHR API is FHIR R4 but client is on older version | Auth fails or endpoints missing | Investigate middleware options (e.g., Redox, Mirth Connect); update timeline |
| Rate limits too restrictive for real-time chat | Calls throttled during testing | Cache availability data; fetch on schedule rather than on-demand |
| Appointment write-back creates duplicate bookings | Duplicate entries in EHR | Implement idempotency key; add duplicate check before write |
| PHI passes through an unapproved service | Compliance flag in review | Immediate stop; re-architect data flow before proceeding |

---

## Execution Tools

- `execution/launch_readiness_tracker.py` — tracks integration items as readiness criteria

---

## Learnings Log

> Update this section as the engagement progresses.

- *(none yet — engagement not started)*
