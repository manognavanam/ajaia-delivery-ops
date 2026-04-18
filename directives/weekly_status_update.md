# Directive: Weekly Client Status Update

**Owner:** AI Solutions Architect (Ajaia)  
**Cadence:** Every Friday EOD  
**Audience:** Client DRI + hospital operations leadership

---

## Goal

Produce a concise, structured weekly status update that gives the client clear visibility into progress, risks, and decisions needed — without requiring them to dig through project files.

---

## Inputs Required

| Input | Source |
|---|---|
| Workstream completion data (milestone status per WS) | `execution/launch_readiness_tracker.py` output |
| Open risks and blockers | Risk register (delivery operating model) |
| Decisions made this week | Delivery lead notes |
| Decisions needed next week | Delivery lead notes |
| Overall RAG status (Red/Amber/Green) | Delivery lead judgment |

---

## Steps

1. Run `execution/generate_status_update.py` with current workstream data as input
2. Review generated output — adjust tone and any inaccurate auto-generated text
3. Add human judgment: what's the real story? What is the evaluator missing?
4. Send to client DRI by Friday 5pm

---

## Output Format

```
Subject: [Project Name] Weekly Status — Week [N] of 8

OVERALL STATUS: [GREEN / AMBER / RED]

PROGRESS THIS WEEK
- [Bullet: what was completed]

UPCOMING PRIORITIES
- [Bullet: what's next]

RISKS & BLOCKERS
- [Risk]: [Status] — [Mitigation in progress]

DECISIONS NEEDED
- [Decision]: [Context] — [Needed by date]
```

---

## Edge Cases & Flags

- **Overall status is RED** → Call the client DRI before sending the written update. The written update follows the call, not the other way around.
- **No decisions needed** → Still include the section, write "None this week." Consistency builds trust.
- **Client hasn't responded to a prior decision request** → Re-surface it in the current update with a deadline.

---

## Execution Tools

- `execution/generate_status_update.py` — generates draft status update from structured workstream inputs

---

## Learnings Log

> Update this section as the engagement progresses.

- *(none yet — engagement not started)*
