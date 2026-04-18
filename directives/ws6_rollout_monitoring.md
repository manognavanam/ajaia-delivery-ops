# Directive: WS-6 Rollout & Performance Monitoring

**Workstream:** WS-6  
**Owner:** Ajaia Delivery Lead + Client Operations + IT  
**Timeline:** Weeks 7–8 (pilot); ongoing post-engagement  
**Dependency:** WS-5 go/no-go sign-off (HARD GATE)

---

## Goal

Launch the agent with a controlled pilot cohort, establish a performance monitoring rhythm, and produce a data-backed recommendation for full rollout.

---

## Inputs Required

| Input | Source | Required By |
|---|---|---|
| WS-5 launch criteria checklist (all green) | WS-5 output | Before pilot go-live |
| Pilot cohort definition (2 providers, 2 appt types) | Client Ops | Week 6 |
| Rollback plan (how to disable agent in < 15 min) | Ajaia Eng | Before go-live |
| Staff training completion confirmation | Client Ops | Before go-live |
| Monitoring dashboard live | Ajaia Eng | Before go-live |

---

## Steps

1. **Pre-launch checklist review** — 48 hours before go-live: verify all WS-5 items green, rollback plan tested, staff briefed.
2. **Pilot go-live** — Enable agent for pilot cohort. Monitor actively for first 4 hours.
3. **Daily monitoring (Week 7)** — Review conversation logs, error rates, escalation rates daily. Triage any issues same day.
4. **Weekly performance review** — Run `execution/generate_status_update.py` to produce weekly report. Share with client DRI.
5. **Agent tuning** — Based on real conversations: update KB gaps, adjust escalation thresholds, refine response quality.
6. **Pilot retrospective (Week 8)** — Analyze pilot metrics vs. baseline. Produce full rollout recommendation with scope, timeline, and risk profile.

---

## Outputs

- [ ] Pilot go-live confirmation (date, cohort, channels active)
- [ ] Daily monitoring log (Week 7)
- [ ] Weekly performance dashboard (response rate, scheduling conversion, escalation rate, patient complaints)
- [ ] Agent tuning log (what was changed, why, what improved)
- [ ] Pilot retrospective document
- [ ] Full rollout recommendation

---

## Key Metrics to Track

| Metric | Definition | Target (Pilot) |
|---|---|---|
| Response rate | % of outreach attempts that receive a patient reply | > 30% |
| Scheduling conversion | % of engaged patients who complete booking | > 25% |
| Escalation rate | % of conversations handed off to human | < 20% |
| Unresolved rate | % of conversations with no resolution (no booking, no escalation) | < 10% |
| Latency P95 | 95th percentile response time for chat/SMS | < 5 seconds |
| Patient complaints | Count of negative feedback or opt-outs | Track; no target set for pilot |

---

## Edge Cases & Flags

- **Escalation rate > 30% in first 48 hours** → Pause outreach. Review conversation logs. Likely a KB gap or conversation flow issue. Return to WS-4.
- **Patient complaints about unsolicited contact** → Immediate audit of consent records. Pause dormant list outreach pending review.
- **Calendar integration creates double bookings** → Roll back scheduling writes immediately. Escalate to WS-3. Revert to human-in-the-loop booking until fixed.
- **Agent goes off-topic or provides clinical information** → Immediate prompt update. Log as critical defect. Notify client compliance.

---

## Execution Tools

- `execution/launch_readiness_tracker.py` — final gate review before go-live
- `execution/generate_status_update.py` — weekly status report generation

---

## Learnings Log

> Update this section as the engagement progresses.

- *(none yet — engagement not started)*
