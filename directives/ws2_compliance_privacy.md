# Directive: WS-2 Compliance & Privacy Review

**Workstream:** WS-2  
**Owner:** Ajaia Compliance Lead + Client Legal/Privacy Officer  
**Timeline:** Weeks 2–3 (runs parallel to WS-1 closeout)  
**Status:** HARD GATE — WS-3 cannot start until this workstream is complete

---

## Goal

Ensure all PHI handling, outreach consent, and data governance requirements are resolved and documented before any patient data enters the AI system.

---

## Inputs Required

| Input | Source | Required By |
|---|---|---|
| Client's existing BAA template or legal contact | Client Legal | Week 1 |
| List of PHI fields the agent will touch (from WS-1 data dictionary) | WS-1 output | Week 2 |
| Data residency requirements (US-only? Specific cloud region?) | Client IT/Legal | Week 2 |
| Existing patient consent records format and coverage | Client CRM admin | Week 2 |
| State-specific outreach regulations (SMS TCPA, email CAN-SPAM) | Ajaia Compliance | Week 2 |

---

## Steps

1. **BAA initiation** — Send BAA to client legal for review. Do not pass Go without this.
2. **PHI field audit** — Using WS-1 data dictionary, classify every field: Is it PHI? Does it need encryption at rest? In transit?
3. **Data flow diagram** — Map exactly where PHI flows: source system → integration layer → AI agent → outbound channel → storage. No ambiguity.
4. **Consent mechanism design** — Confirm client has valid opt-in consent for each outreach channel. Design opt-out capture in the agent's first message.
5. **Retention policy** — Define what the agent stores, for how long, and deletion mechanism.
6. **Compliance sign-off checklist** — Walk through with client legal. Get written sign-off.

---

## Outputs

- [ ] Executed Business Associate Agreement (BAA)
- [ ] PHI data flow diagram (approved by client legal)
- [ ] Consent/opt-out mechanism design
- [ ] Data retention and deletion policy
- [ ] Compliance sign-off checklist (all items green)

---

## Edge Cases & Flags

- **BAA negotiation takes longer than 1 week** → Escalate immediately. This blocks the entire build. Explore if a limited test using synthetic data is permissible as a parallel track.
- **Client consent records are incomplete** → Agent cannot reach unconsented leads. Scope pilot to consented leads only. Raise as RISK-03.
- **State-specific SMS regulations are unclear** → Default to most restrictive interpretation. Flag for legal review before sending first outreach batch.
- **Client uses a cloud provider not approved for PHI** → Requires architecture change in WS-3. Flag immediately — this affects integration design.

---

## Execution Tools

- `execution/launch_readiness_tracker.py` — compliance items tracked as launch-readiness criteria

---

## Learnings Log

> Update this section as the engagement progresses.

- *(none yet — engagement not started)*
