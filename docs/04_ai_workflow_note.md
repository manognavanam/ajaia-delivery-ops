# AI Workflow Note
## Patient Acquisition & Growth Agent — Ajaia Take-Home Assignment
**Author:** Manogna Vanam | **Date:** April 18, 2026

---

## Overview

AI tools were used throughout this assignment — not as a shortcut, but as an execution accelerator at each layer of the DOE framework. Every output was reviewed, refined, and owned. This note is honest about where AI added speed and where human judgment was the actual work.

---

## Tools Used

| Tool | How Used |
|---|---|
| **Claude (Sonnet 4.6 via Claude Code)** | Primary AI assistant — orchestration layer for the entire assignment |
| **Claude (Haiku 4.5 via Anthropic API)** | Powers the "Generate Delivery Insights" feature inside the Streamlit prototype |
| **Streamlit** | Python framework for the prototype UI |

---

## How AI Was Used at Each Layer

### Layer 1 — Directives (SOPs)
Claude drafted the initial structure of all 6 workstream directives based on my scenario framing. I reviewed each one for healthcare-specific accuracy — for example, adding the distinction between FHIR R4 and proprietary EHR APIs in WS-3, tightening the HIPAA language in WS-2, and adding the "clinical no-go zones" guardrail in WS-4. AI produced the skeleton; I made the judgment calls about what actually matters in a healthcare AI deployment.

### Layer 2 — Orchestration (Delivery Planning)
I used Claude Code as a live planning partner throughout — asking it to structure workstreams, sequence milestones, and identify risk interdependencies. When I realized mid-session that we weren't following the DOE framework (Directives → Orchestration → Execution), I course-corrected the structure entirely. That decision — and knowing *why* the framework matters — was mine.

The risk register was co-developed: I seeded it with the high-probability failure modes I've seen in healthcare integrations (EHR API delays, PHI consent gaps, escalation routing gaps), and Claude helped articulate the monitoring and mitigation language consistently.

### Layer 3 — Execution (Prototype)
Claude Code wrote the Streamlit prototype in `execution/launch_readiness_tracker.py` and `execution/generate_status_update.py`. I specified the exact data structures (workstream states, launch criteria, risks, open items), the 5-tab layout, the 3-column header design, and the AI insights panel architecture. When the layout broke (badges wrapping, status note truncating), I diagnosed the issue and directed the fix.

The "Generate Delivery Insights" feature uses a real Anthropic API call to Claude Haiku. I wrote the prompt structure — the exact format (PROJECT SUMMARY / KEY RISKS / RECOMMENDED NEXT ACTIONS) and the instruction to be specific about owners and dates, not generic. The prompt is the orchestration layer inside the execution layer.

---

## What AI Accelerated

- **Document scaffolding** — Getting from blank page to structured first draft in minutes, not hours
- **Consistent formatting** — All 6 directives follow the same structure (goal, inputs, steps, outputs, edge cases, learnings log) without drift
- **Code iteration** — Layout fixes, indentation errors, HTML styling adjustments resolved in seconds
- **Cross-referencing** — Keeping the prototype data consistent with the delivery operating model (same risk IDs, same workstream names, same milestone dates)

**Estimated time saved: ~2.5 hours** of the 4-hour budget. That time went into thinking — what does a hospital client actually care about? What fails in EHR integrations? What makes a risk register credible vs. generic?

---

## What Was Mine

- **The DOE framework application** — Recognizing that flat markdown docs weren't enough and restructuring around Directives → Orchestration → Execution
- **Healthcare domain specificity** — FHIR versioning, BAA sequencing, PHI field classification, SMS TCPA compliance, clinical no-go guardrails
- **Assumption quality** — The assumption set (latency requirements, consent ownership, guardrails, AI scope boundary) was materially better than the first draft and reflects real delivery thinking
- **Pilot scope decision** — Choosing 2 providers / 2 appointment types as the right blast radius for a first live test
- **Risk prioritization** — Deciding which risks are truly critical (EHR API delay, BAA gap) vs. monitoring-only (lead data quality, agent response quality)
- **Prototype UX decisions** — 3-column header, status legend placement, "done when" criteria per workstream, AI insights panel layout
- **Every review and rejection** — Multiple AI outputs were discarded or substantially rewritten when they were too generic, too safe, or missed the healthcare context

---

## Honest Assessment

This assignment took approximately 3.5 hours with AI assistance. Without it, the same quality output would have taken 7–8 hours. The AI didn't make the work easier to *think* — it made it faster to *produce*. The thinking — what matters, what's realistic, what would actually fail — was the actual work.

The prototype (`execution/launch_readiness_tracker.py`) is a real tool a delivery team could use on Day 1 of this engagement. That's the bar AI-native execution should be held to: not "did you use AI?" but "would this be useful in production?"
