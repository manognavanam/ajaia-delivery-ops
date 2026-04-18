# Patient Acquisition & Growth Agent — Delivery Ops
**Ajaia AI Consultancy | Take-Home Assignment**  
**Delivery Lead:** Manogna Vanam

---

## What This Is

A delivery operations system for the **Patient Acquisition & Growth Agent** engagement — a hospital client implementing an AI agent that engages inbound and dormant patient leads and books appointments directly into provider calendars.

Built using the **DOE framework (Directives → Orchestration → Execution)**:
- `directives/` — SOPs per workstream (living documents, updated as the engagement progresses)
- `execution/` — Deterministic Python scripts (the prototype and status generator)
- `docs/` — Human-readable submission deliverables

---

## Quickstart

```bash
# 1. Clone / download the project
cd Ajaia

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key (optional — mock fallback works without it)
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your-key-here

# 5. Launch the delivery dashboard
streamlit run execution/launch_readiness_tracker.py

# 6. Generate a weekly status update
python execution/generate_status_update.py
```

Dashboard opens at **http://localhost:8501**

---

## Project Structure

```
Ajaia/
│
├── CLAUDE.md / AGENTS.md / GEMINI.md   # DOE framework instructions (AI-readable)
├── README.md                            # This file
├── requirements.txt                     # Python dependencies
├── .env.example                         # Secrets template (safe to share)
├── .env                                 # Real secrets (gitignored — never commit)
│
├── directives/                          # Layer 1: SOPs (what to do)
│   ├── ws1_discovery_requirements.md
│   ├── ws2_compliance_privacy.md
│   ├── ws3_integrations_scheduling.md
│   ├── ws4_conversation_design.md
│   ├── ws5_qa_pilot_readiness.md
│   ├── ws6_rollout_monitoring.md
│   └── weekly_status_update.md
│
├── execution/                           # Layer 3: Scripts (doing the work)
│   ├── launch_readiness_tracker.py      # Streamlit dashboard (main prototype)
│   ├── generate_status_update.py        # Weekly client status report generator
│   └── data/                            # Intermediate data (regenerable)
│
├── docs/                                # Submission deliverables
│   ├── 01_delivery_operating_model.md   # Part 1: Workstreams, milestones, risks
│   ├── 02_technical_readiness_note.md   # Part 2: WS-3 technical readiness
│   ├── 03_client_status_update.md       # Part 4: Sample weekly update
│   ├── 04_ai_workflow_note.md           # Part 5: AI tool usage
│   └── workstream_diagram.svg           # Dependency diagram
│
└── .tmp/                                # Temp files (gitignored, regenerable)
```

---

## The Prototype: What It Does

### `execution/launch_readiness_tracker.py`
A Streamlit dashboard with 5 tabs:

| Tab | What it shows |
|---|---|
| **Workstream Health** | Completion % per workstream, blockers, "done when" criteria |
| **Launch Criteria** | 12 go/no-go gates with pass/fail/pending status |
| **Risk Register** | 6 risks sorted by severity, with mitigation detail |
| **Milestones** | Week 1–8 timeline with current week highlighted |
| **Open Items** | Active blockers (red) and pending decisions (amber) |

**AI Insights panel** (right side): Click "Generate Delivery Insights" to get a Claude-powered analysis of the current engagement state — project summary, top risks, and recommended next actions. Requires `ANTHROPIC_API_KEY` in `.env`; falls back to mock output if not set.

**Header**: Three side-by-side boxes — delivery status (RAG), overall status guide, and workstream status guide — so any team member understands the color coding at a glance.

### `execution/generate_status_update.py`
Generates a structured weekly client status update from workstream data. Prints to console and saves to `.tmp/status_update_weekN.txt`.

```bash
python execution/generate_status_update.py
```

---

## The Directives: How to Use Them

Each directive in `directives/` is a living SOP for one workstream. As the engagement progresses:

1. Update the **Learnings Log** at the bottom of each directive when you discover something new
2. Update the **completion status** in `execution/launch_readiness_tracker.py` → `WORKSTREAMS` data block
3. The dashboard reflects the new state immediately on next load

The directives are also readable inside the app — open any workstream expander in the sidebar to see the "done when" criteria and a "Show full directive" button.

---

## Submission Documents

| File | Part |
|---|---|
| `docs/01_delivery_operating_model.md` | Part 1 — Delivery Operating Model |
| `docs/02_technical_readiness_note.md` | Part 2 — Technical Readiness Note (WS-3) |
| `execution/launch_readiness_tracker.py` | Part 3 — Coded Prototype |
| `docs/03_client_status_update.md` | Part 4 — Sample Client Status Update |
| `docs/04_ai_workflow_note.md` | Part 5 — AI Workflow Note |

---

## Requirements

- Python 3.9+
- All dependencies in `requirements.txt` (Streamlit, pandas, anthropic, python-dotenv)
- `ANTHROPIC_API_KEY` in `.env` for live AI insights (optional — mock works without it)
