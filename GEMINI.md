# Agent Instructions

> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**
- SOPs written in Markdown, live in `directives/`
- Define the goals, inputs, tools/scripts to use, outputs, and edge cases
- Natural language instructions, like you'd give a mid-level employee
- Each workstream in this engagement has its own directive file

**Layer 2: Orchestration (Decision making)**
- This is you. Your job: intelligent routing.
- Read directives, call execution tools in the right order, handle errors, ask for clarification, update directives with learnings
- You're the glue between intent and execution — you don't manually process data yourself, you read the relevant directive and run the appropriate script in `execution/`

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Environment variables and API tokens stored in `.env` (never committed)
- Handle data processing, file operations, API calls, report generation
- Reliable, testable, fast. Use scripts instead of manual work.

**Why this works:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. The solution is to push complexity into deterministic code. That way the LLM just focuses on decision-making.

---

## Project Context

**Engagement:** Patient Acquisition & Growth Agent — Hospital Client  
**Ajaia Role:** Lead delivery and AI orchestration layer  
**Client Role:** Owns EHR/CRM system-of-record integrations

**Active Directives:**
- `directives/ws1_discovery_requirements.md` — Discovery & Requirements
- `directives/ws2_compliance_privacy.md` — Compliance & Privacy (HIPAA gate)
- `directives/ws3_integrations_scheduling.md` — CRM/EHR integrations
- `directives/ws4_conversation_design.md` — Agent conversation flows
- `directives/ws5_qa_pilot_readiness.md` — QA and launch criteria
- `directives/ws6_rollout_monitoring.md` — Pilot go-live and monitoring
- `directives/weekly_status_update.md` — Weekly client status report

**Execution Tools:**
- `execution/launch_readiness_tracker.py` — Streamlit dashboard tracking all launch criteria
- `execution/generate_status_update.py` — Generates weekly client status update from workstream data

---

## Operating Principles

**1. Check for tools first**
Before writing a script, check `execution/`. Only create new scripts if none exist for the task.

**2. Self-anneal when things break**
- Read the error message and stack trace
- Fix the script and test again
- Update the relevant directive with what you learned

**3. Update directives as you learn**
Directives are living documents. When you discover constraints, better approaches, or edge cases — update the directive.

---

## Self-Annealing Loop

When something breaks:
1. Fix it
2. Update the tool
3. Test — confirm it works
4. Update the directive
5. System is now stronger

---

## File Organization

```
directives/      ← SOPs per workstream (living documents)
execution/       ← Deterministic Python scripts
execution/data/  ← Intermediate data files (regenerable)
.tmp/            ← Temporary processing files (never commit)
docs/            ← Human-readable submission deliverables
.env             ← API keys and secrets (never commit)
requirements.txt ← Python dependencies
```

---

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.
