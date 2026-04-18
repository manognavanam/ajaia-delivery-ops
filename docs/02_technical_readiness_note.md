# Technical Readiness Note
## WS-3: Integrations & Scheduling Systems
**Engagement:** Patient Acquisition & Growth Agent — Hospital Client  
**Prepared by:** Manogna Vanam | **Date:** April 18, 2026  
**Directive:** `directives/ws3_integrations_scheduling.md`

---

## Why This Workstream

WS-3 is the highest-risk workstream in this engagement. It sits at the center of the dependency graph — blocked by compliance (WS-2), and blocking both QA (WS-5) and go-live (WS-6). Integration delays are the single most common cause of healthcare AI project slippage. This note defines exactly what "ready to build" means so the team does not start before the right inputs are in place.

---

## What This Workstream Must Deliver

Three technical connections, all tested in staging before WS-5 begins:

| Connection | Direction | Purpose |
|---|---|---|
| CRM ↔ Agent | Bidirectional | Pull lead records; write outreach status back |
| EHR/Scheduling ↔ Agent | Bidirectional | Read provider availability; write confirmed appointments |
| Outreach channels (SMS/Email) | Outbound + inbound | Send patient messages; receive replies and opt-outs |

---

## Technical Inputs Required

### From Client IT
| Input | Format | Required By | Notes |
|---|---|---|---|
| CRM API documentation | PDF or URL | Week 3, Day 1 | Need endpoint list, auth method, rate limits |
| CRM sandbox credentials | OAuth tokens or API key | Week 3, Day 1 | Must have write access for status updates |
| EHR scheduling API documentation | PDF or URL | Week 3, Day 1 | FHIR R4 preferred; confirm version |
| EHR sandbox credentials | OAuth or API key | Week 3, Day 1 | Read: availability slots. Write: appointments |
| Staging/test environment access | VPN or IP whitelist | Before build starts | Ajaia IPs to be whitelisted |
| Appointment booking rules document | Written spec | Week 3 | Slot duration, buffer times, provider preferences, overbooking policy |

### From WS-2 (Compliance Gate — Hard Block)
| Input | Required Before |
|---|---|
| Executed BAA | Any PHI-touching code is written |
| Approved list of PHI fields the agent may read/write | Integration data model is defined |
| Data residency confirmation (cloud region) | Infrastructure is provisioned |

### From WS-1 (Discovery Output)
| Input | Notes |
|---|---|
| Data dictionary | Field-level mapping between CRM schema and agent data model |
| Appointment types in scope | Drives the calendar query logic |
| Lead segment definitions (inbound vs. dormant) | Determines CRM filter criteria |

### Ajaia-Owned Inputs
| Input | Notes |
|---|---|
| Outreach channel account (Twilio or equivalent) | Ajaia provisions; needs client phone number or sender ID |
| Email provider setup (SendGrid or equivalent) | Ajaia provisions; client domain for sender address |
| Agent data model schema | Defined by Ajaia engineering based on WS-1 data dictionary |

---

## Systems and Teams That Must Be Involved

| System | Team | Role |
|---|---|---|
| CRM (e.g., Salesforce, HubSpot, Epic Referral Mgmt) | Client IT | API access, sandbox, field permissions |
| EHR / Scheduling platform (e.g., Epic, Athenahealth) | Client IT + Clinical Ops | API access, booking rules sign-off |
| Outreach layer (Twilio SMS, SendGrid email) | Ajaia Engineering | Provisioning, sender ID, opt-out webhook |
| AI orchestration layer | Ajaia Engineering | Integration adapter, data transformation, error handling |
| Compliance / Legal | Client Legal + Ajaia Compliance | PHI field approval before build; BAA must be executed |

**Minimum viable team for a WS-3 build kickoff:**
- Ajaia Engineering Lead
- Client IT representative with API/admin access to both CRM and EHR
- Ajaia Compliance Lead (to confirm PHI boundary before first data call)

---

## Questions That Must Be Answered Before Build Begins

### CRM Integration
1. What CRM system is in use, and what version? Is the API REST or SOAP?
2. What authentication method does it use — OAuth 2.0, API key, or session token?
3. What are the rate limits (calls per minute/hour)?
4. Which fields constitute a "lead record"? What is the unique identifier?
5. What status values exist in the CRM for lead progression (e.g., New → Contacted → Scheduled → No-Show)?
6. Does the CRM support webhook events, or must we poll for changes?

### EHR / Scheduling Integration
7. Which EHR and scheduling system is in use? What version of the API (FHIR R4? Proprietary)?
8. Does the scheduling system have a sandbox/test environment that mirrors production data structure?
9. How is provider availability exposed — as a FHIR Schedule/Slot resource, a proprietary endpoint, or a flat export?
10. What is the appointment write mechanism — a POST to a booking endpoint, or a workflow that requires human confirmation?
11. Are there any scheduling rules that the API does not enforce (e.g., buffer times, provider preferences) that we must implement in the agent layer?
12. What happens if a slot is booked simultaneously by two callers — does the EHR handle conflicts, or must we?

### Outreach Channels
13. Does the client have an existing Twilio account or preferred SMS provider?
14. What phone number or short code will outreach messages originate from?
15. What is the client's process for managing opt-outs — does the CRM track them, or is it handled at the channel level?
16. Are there time-of-day restrictions on outreach (e.g., no SMS before 8am or after 8pm)?

### Data and Compliance
17. Has the client confirmed which cloud region patient data may reside in?
18. Are there fields in the CRM or EHR that are off-limits even with a BAA (e.g., behavioral health, substance use records)?
19. What is the maximum retention period for any data the agent temporarily stores?

---

## What Could Go Wrong Technically

| Risk | Likelihood | Impact | Early Signal | Response |
|---|---|---|---|---|
| EHR API is older version (non-FHIR) or has no sandbox | High | High | No sandbox URL provided by Week 3 | Evaluate middleware (Redox, Mirth Connect); adjust timeline |
| CRM API rate limits too low for real-time use | Medium | High | Throttle errors in first test | Implement caching + async polling; renegotiate with client IT |
| Slot availability not exposed via API — only UI | Medium | Critical | API docs show no read endpoint | Escalate to EHR vendor; consider screen-scraping fallback (fragile) or manual export |
| Appointment write creates duplicate bookings | Low | Critical | Duplicate entries in staging EHR | Add idempotency key; implement pre-write duplicate check |
| PHI flows through unapproved intermediate service | Low | Critical | Compliance review flags a field | Stop immediately; re-architect data path before proceeding |
| OAuth tokens expire mid-session | Medium | Medium | Auth errors in staging after hour 1 | Implement token refresh logic; test token lifecycle explicitly |
| Client IT cannot provide sandbox — only production access | Medium | High | No sandbox URL by Day 3 | Hard stop on live testing; escalate; do not write to production EHR |

---

## "Ready to Build" Definition

Build does not start until **all** of the following are confirmed:

| Gate | Owner | Confirmed? |
|---|---|---|
| CRM sandbox credentials delivered and authentication validated | Client IT | ⬜ |
| EHR sandbox credentials delivered and authentication validated | Client IT | ⬜ |
| API rate limits documented | Client IT | ⬜ |
| Appointment booking rules written and signed off by clinical ops | Client Clinical Ops | ⬜ |
| PHI field list approved by compliance | Ajaia Compliance | ⬜ |
| BAA executed | Client Legal | ⬜ |
| Data residency confirmed | Client Legal / IT | ⬜ |
| Rollback plan defined (how to disable integration in < 15 min) | Ajaia Engineering | ⬜ |

**If any gate is open: do not build. Surface the gap, escalate to DRI, and document the timeline impact.**

---

## Execution Script

This workstream's completion state is tracked in real-time via:

```bash
streamlit run execution/launch_readiness_tracker.py
```

All "Ready to Build" gates above map to items in the **Launch Criteria** tab. WS-3 completion feeds directly into the WS-5 QA trigger.
