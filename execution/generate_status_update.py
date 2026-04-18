"""
execution/generate_status_update.py

Directive: directives/weekly_status_update.md
Purpose:   Generate a structured weekly client status update from workstream data.
           Output is printed to console and saved to .tmp/status_update_weekN.txt
Run:       python execution/generate_status_update.py
"""

import os
from datetime import date

# ─────────────────────────────────────────────
# INPUT — update each week before running
# ─────────────────────────────────────────────

STATUS = {
    "project": "Patient Acquisition & Growth Agent",
    "client": "Hospital Client",
    "week": 3,
    "total_weeks": 8,
    "date": str(date.today()),
    "overall_rag": "AMBER",  # GREEN | AMBER | RED
    "delivery_lead": "Manogna Vanam",
}

PROGRESS_THIS_WEEK = [
    "Completed discovery and requirements sign-off (WS-1 closed). Requirements document approved by client ops and IT.",
    "PHI fields classified and data flow diagram drafted (WS-2 in progress). BAA sent to client legal — response expected in 3 business days.",
    "CRM API connected and authenticated in staging environment. Lead ingestion from CRM validated end-to-end.",
    "Inbound inquiry and dormant re-engagement conversation flows drafted (WS-4). Escalation playbook sent to client clinical ops for review.",
    "Single client DRI confirmed (VP Operations). Weekly check-in cadence established every Monday at 10am.",
]

UPCOMING_PRIORITIES = [
    "Execute BAA with client legal (WS-2 gate — blocks WS-3 build start).",
    "Obtain EHR sandbox credentials from client IT and begin calendar API integration (WS-3).",
    "Complete conversation flow review session with client clinical ops and finalize knowledge base (WS-4).",
    "Conduct data quality audit on dormant lead list ahead of pilot scoping.",
    "Deliver Technical Design Checkpoint document to client by end of week.",
]

RISKS_AND_BLOCKERS = [
    {
        "item": "EHR sandbox credentials not yet delivered",
        "severity": "HIGH",
        "status": "ACTIVE BLOCKER",
        "action": "Escalated to client DRI. Using CSV export as temporary CRM fallback. Client IT has committed to delivery by April 20.",
    },
    {
        "item": "BAA under legal review",
        "severity": "HIGH",
        "status": "MONITORING",
        "action": "Client legal has document. Following up daily. No build on PHI data paths until signed.",
    },
    {
        "item": "Escalation routing rules not yet finalized",
        "severity": "MEDIUM",
        "status": "MONITORING",
        "action": "Playbook in client clinical ops review. Decision needed by April 25 to stay on schedule for WS-4 sign-off.",
    },
]

DECISIONS_NEEDED = [
    {
        "decision": "EHR sandbox credentials delivery",
        "context": "Required to begin calendar API integration. Currently blocking WS-3 and compressing QA timeline if delayed further.",
        "needed_by": "April 20, 2026",
        "owner": "Client IT / VP Operations",
    },
    {
        "decision": "Escalation routing confirmation",
        "context": "Who receives escalated conversations (role and channel)? Required before conversation design can be finalized.",
        "needed_by": "April 25, 2026",
        "owner": "Client Clinical Ops",
    },
    {
        "decision": "Pilot provider cohort selection",
        "context": "Need names of 2 providers and 2 appointment types for the Week 7 pilot. Scheduling rules vary by provider.",
        "needed_by": "April 28, 2026",
        "owner": "Client Operations",
    },
]

# ─────────────────────────────────────────────
# GENERATOR
# ─────────────────────────────────────────────

def build_status_update(s, progress, upcoming, risks, decisions):
    rag = s["overall_rag"]
    rag_symbol = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}.get(rag, "⚪")

    lines = []
    lines.append("=" * 70)
    lines.append(f"  {s['project']}")
    lines.append(f"  Weekly Status Update — Week {s['week']} of {s['total_weeks']}")
    lines.append(f"  {s['date']}  |  Delivery Lead: {s['delivery_lead']}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"OVERALL STATUS:  {rag_symbol} {rag}")
    lines.append("")
    lines.append("─" * 70)
    lines.append("PROGRESS THIS WEEK")
    lines.append("─" * 70)
    for item in progress:
        lines.append(f"  • {item}")
    lines.append("")

    lines.append("─" * 70)
    lines.append("UPCOMING PRIORITIES (Next 7 Days)")
    lines.append("─" * 70)
    for item in upcoming:
        lines.append(f"  • {item}")
    lines.append("")

    lines.append("─" * 70)
    lines.append("RISKS & BLOCKERS")
    lines.append("─" * 70)
    for r in risks:
        lines.append(f"  [{r['severity']}] {r['item']}")
        lines.append(f"    Status: {r['status']}")
        lines.append(f"    Action: {r['action']}")
        lines.append("")

    lines.append("─" * 70)
    lines.append("DECISIONS NEEDED FROM CLIENT")
    lines.append("─" * 70)
    for d in decisions:
        lines.append(f"  ► {d['decision']}")
        lines.append(f"    Context:    {d['context']}")
        lines.append(f"    Needed by:  {d['needed_by']}")
        lines.append(f"    Owner:      {d['owner']}")
        lines.append("")

    lines.append("─" * 70)
    lines.append(f"Next update: Week {s['week'] + 1}  |  Questions: {s['delivery_lead']}")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_to_tmp(content, week):
    os.makedirs(".tmp", exist_ok=True)
    path = f".tmp/status_update_week{week}.txt"
    with open(path, "w") as f:
        f.write(content)
    return path


if __name__ == "__main__":
    update = build_status_update(STATUS, PROGRESS_THIS_WEEK, UPCOMING_PRIORITIES,
                                  RISKS_AND_BLOCKERS, DECISIONS_NEEDED)
    print(update)
    saved = save_to_tmp(update, STATUS["week"])
    print(f"\n[Saved to {saved}]")
