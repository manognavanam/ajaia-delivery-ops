"""
execution/launch_readiness_tracker.py

Directive: directives/ws5_qa_pilot_readiness.md
Purpose:   Internal delivery dashboard for the Patient Acquisition & Growth Agent.
           Tracks workstream health, launch criteria, risks, and open blockers.
           Includes AI-powered delivery insights via Anthropic Claude.
Run:       streamlit run execution/launch_readiness_tracker.py
"""

import os
import streamlit as st
from datetime import date
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────
# AI INSIGHTS — real Claude call, mock fallback
# ─────────────────────────────────────────────

def build_prompt(engagement, workstreams, risks, open_items, launch_criteria):
    blockers = [i for i in open_items if i["blocker"]]
    criteria_fail_count = sum(1 for _, _, s in launch_criteria if s is False)

    ws_summary = "\n".join(
        f"  - {w['id']} {w['name']}: {w['status']} ({w['pct']}%) — {w['note']}"
        for w in workstreams
    )
    risk_summary = "\n".join(
        f"  - [{r['severity']}] {r['title']}: {r['status']} — {r['mitigation']}"
        for r in risks
    )
    blocker_summary = "\n".join(
        f"  - {i['item']} (Owner: {i['owner']}, Due: {i['due']})"
        for i in blockers
    ) or "  None"

    return f"""You are an AI delivery advisor for Ajaia, an AI consultancy.
Analyze the current state of this engagement and provide concise, actionable insights.

ENGAGEMENT: {engagement['name']} — {engagement['client']}
Week {engagement['current_week']} of {engagement['total_weeks']} | Overall Status: {engagement['overall_status']}
Delivery Lead: {engagement['delivery_lead']}

WORKSTREAMS:
{ws_summary}

RISKS:
{risk_summary}

ACTIVE BLOCKERS:
{blocker_summary}

FAILING LAUNCH CRITERIA: {criteria_fail_count} items failing

Respond in exactly this format — no extra text, no markdown headers beyond what's shown:

PROJECT SUMMARY
[2-3 sentences: current state of the engagement, what's on track, what's at risk]

KEY RISKS RIGHT NOW
1. [Most urgent risk and why]
2. [Second risk]
3. [Third risk]

RECOMMENDED NEXT ACTIONS
1. [Specific action, who should do it, by when]
2. [Specific action, who should do it, by when]
3. [Specific action, who should do it, by when]"""


def get_api_key():
    """Check st.secrets first (Streamlit Cloud), then .env (local)."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY")


def call_claude(prompt):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=get_api_key())
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text, "claude-haiku-4-5"
    except Exception as e:
        return None, str(e)


def mock_insights():
    return """PROJECT SUMMARY
The engagement is in Week 3 of 8 with WS-1 complete and WS-2/WS-4 progressing on schedule. The primary risk is WS-3 integration build, currently blocked on EHR sandbox credentials from client IT — a 2-day delay that, if unresolved by April 20, will compress QA and threaten the Week 7 pilot date. All other workstreams are tracking to plan.

KEY RISKS RIGHT NOW
1. EHR credential delay (ACTIVE BLOCKER): Client IT has not delivered sandbox access. Every day of delay directly reduces WS-3 build time and compresses WS-5 QA. Escalate to VP Operations today.
2. BAA not yet executed: No PHI-touching integration code can be written without the signed BAA. Legal review must close this week or the compliance gate will slip into WS-3's build window.
3. Escalation routing undefined: Conversation design cannot be finalized until client clinical ops confirms who receives escalated patient conversations. This risks WS-4 overrunning into WS-5 time.

RECOMMENDED NEXT ACTIONS
1. Ajaia SA: Call VP Operations today to escalate EHR credential delivery — do not wait for the Monday standup. Get a committed hour, not a date.
2. Ajaia Compliance Lead: Follow up with client legal on BAA daily. Offer to schedule a 30-min call to resolve any redlines this week.
3. Ajaia AI Designer: Schedule escalation routing sign-off session with client clinical ops before April 25 — send the calendar invite now, don't wait for their confirmation.""", "mock"


def generate_insights(engagement, workstreams, risks, open_items, launch_criteria):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return mock_insights()
    prompt = build_prompt(engagement, workstreams, risks, open_items, launch_criteria)
    text, source = call_claude(prompt)
    if text:
        return text, source
    return mock_insights()[0], "mock (API error)"


def parse_insights(raw):
    """Split raw text into the three sections."""
    sections = {"summary": "", "risks": "", "actions": ""}
    current = None
    for line in raw.splitlines():
        if line.strip() == "PROJECT SUMMARY":
            current = "summary"
        elif line.strip() == "KEY RISKS RIGHT NOW":
            current = "risks"
        elif line.strip() == "RECOMMENDED NEXT ACTIONS":
            current = "actions"
        elif current:
            sections[current] += line + "\n"
    return {k: v.strip() for k, v in sections.items()}

# ─────────────────────────────────────────────
# DATA — update this as the engagement progresses
# ─────────────────────────────────────────────

ENGAGEMENT = {
    "name": "Patient Acquisition & Growth Agent",
    "client": "Hospital Client",
    "start_date": "2026-04-18",
    "current_week": 3,
    "total_weeks": 8,
    "delivery_lead": "Manogna Vanam",
    "overall_status": "AMBER",  # GREEN | AMBER | RED
    "status_note": "Integration credentials delayed 2 days. BAA under legal review. All other tracks on schedule.",
}

WORKSTREAMS = [
    {
        "id": "WS-1", "name": "Discovery & Requirements",
        "owner": "Ajaia SA + Client Ops", "weeks": "1–2",
        "status": "Complete", "pct": 100,
        "note": "Requirements signed off. Data dictionary finalized.",
        "directive": "directives/ws1_discovery_requirements.md",
        "done_when": [
            "Current-state workflow map delivered",
            "Agent scope document signed off (channels, use cases, escalation rules)",
            "Success metrics baseline captured",
            "Requirements document signed by client ops and IT",
            "Preliminary data dictionary finalized",
        ],
    },
    {
        "id": "WS-2", "name": "Compliance & Privacy",
        "owner": "Ajaia Compliance + Client Legal", "weeks": "2–3",
        "status": "In Progress", "pct": 60,
        "note": "BAA in legal review (ETA 3 days). PHI fields classified. Consent mechanism designed.",
        "directive": "directives/ws2_compliance_privacy.md",
        "done_when": [
            "BAA executed and on file",
            "PHI data flow diagram approved by client legal",
            "Consent/opt-out mechanism designed and signed off",
            "Data retention and deletion policy approved",
            "Compliance sign-off checklist — all items green",
        ],
    },
    {
        "id": "WS-3", "name": "Integrations & Scheduling",
        "owner": "Ajaia Eng + Client IT", "weeks": "3–5",
        "status": "Blocked", "pct": 15,
        "note": "BLOCKED: EHR sandbox credentials not yet delivered by client IT. CRM API connected and tested.",
        "directive": "directives/ws3_integrations_scheduling.md",
        "done_when": [
            "CRM lead ingestion working and status write-back verified",
            "Calendar API: read availability + write appointments tested",
            "SMS and email outreach channels live with opt-out handling",
            "Data mapping specification document complete",
            "End-to-end staging test passed (lead in → slot booked → CRM updated)",
        ],
    },
    {
        "id": "WS-4", "name": "Conversation Design & Knowledge",
        "owner": "Ajaia AI + Client Clinical Ops", "weeks": "3–4",
        "status": "In Progress", "pct": 40,
        "note": "Inbound and dormant flows drafted. Escalation playbook in review with client clinical ops.",
        "directive": "directives/ws4_conversation_design.md",
        "done_when": [
            "All conversation flows designed and client-approved (inbound, dormant, scheduling, escalation)",
            "Knowledge base populated with FAQs, clinic info, appointment prep",
            "Escalation + fallback playbook signed off by client clinical ops",
            "Guardrail definitions documented (clinical no-go zones)",
            "System prompt v1 approved; 10+ sample conversations reviewed",
        ],
    },
    {
        "id": "WS-5", "name": "QA & Pilot Readiness",
        "owner": "Ajaia QA + Client Ops", "weeks": "5–6",
        "status": "Not Started", "pct": 0,
        "note": "Depends on WS-3 and WS-4 completion.",
        "directive": "directives/ws5_qa_pilot_readiness.md",
        "done_when": [
            "Full QA test plan executed — all scenarios pass",
            "Every escalation path tested and verified end-to-end",
            "Staging environment signed off",
            "All 12 launch criteria items green",
            "Known issues log reviewed — no critical or high severity open",
        ],
    },
    {
        "id": "WS-6", "name": "Rollout & Monitoring",
        "owner": "Ajaia Delivery + Client IT", "weeks": "7–8",
        "status": "Not Started", "pct": 0,
        "note": "Depends on WS-5 go/no-go sign-off.",
        "directive": "directives/ws6_rollout_monitoring.md",
        "done_when": [
            "Pilot live for 2 providers, 2 appointment types",
            "Daily monitoring log maintained through Week 7",
            "Weekly performance dashboard shared with client",
            "Agent tuning log — at least one improvement cycle complete",
            "Pilot retrospective delivered with full rollout recommendation",
        ],
    },
]

MILESTONES = [
    {"week": 1, "milestone": "Kickoff & Stakeholder Alignment", "status": "Done"},
    {"week": 2, "milestone": "Current-State Discovery Complete", "status": "Done"},
    {"week": 2, "milestone": "Requirements Baseline Signed Off", "status": "Done"},
    {"week": 3, "milestone": "BAA Executed", "status": "At Risk"},
    {"week": 3, "milestone": "Technical Design Checkpoint", "status": "In Progress"},
    {"week": 4, "milestone": "Integration Build Started", "status": "At Risk"},
    {"week": 4, "milestone": "Conversation Design Review", "status": "In Progress"},
    {"week": 5, "milestone": "Integration Milestone (E2E in staging)", "status": "Upcoming"},
    {"week": 6, "milestone": "Pilot Readiness Review", "status": "Upcoming"},
    {"week": 7, "milestone": "Pilot Go-Live (2 providers, 2 appt types)", "status": "Upcoming"},
    {"week": 8, "milestone": "Pilot Retrospective & Rollout Plan", "status": "Upcoming"},
]

LAUNCH_CRITERIA = [
    # (criterion, owner, status)  status: True=Pass, False=Fail, None=Not Tested
    ("All integration tests pass in staging", "Ajaia Eng", None),
    ("No PHI leaves approved data boundaries", "Ajaia Compliance", None),
    ("BAA executed and on file", "Ajaia Compliance + Client Legal", False),
    ("All conversation flows tested end-to-end", "Ajaia QA", None),
    ("Every escalation trigger routes correctly", "Ajaia QA + Client Ops", None),
    ("Opt-out mechanism tested and confirmed", "Ajaia Eng", None),
    ("Latency < 5s for chat/SMS (P95)", "Ajaia Eng", None),
    ("Client ops staff trained on escalations", "Client Ops", None),
    ("Rollback plan documented and tested", "Ajaia Eng", None),
    ("Client sign-off on sample conversation quality", "Client Clinical Ops", None),
    ("CRM lead sync verified (inbound + dormant)", "Ajaia Eng", None),
    ("Calendar write-back creates no duplicates", "Ajaia Eng", None),
]

RISKS = [
    {
        "id": "R-01", "title": "PHI Handling & HIPAA Gap",
        "severity": "Critical", "probability": "Low",
        "status": "Monitoring",
        "mitigation": "BAA in legal review. PHI fields classified. Compliance gate before WS-3 build.",
    },
    {
        "id": "R-02", "title": "EHR API Access Delayed",
        "severity": "High", "probability": "High",
        "status": "Active",
        "mitigation": "Escalated to client DRI. Using CSV export as temporary fallback. ETA: 2 days.",
    },
    {
        "id": "R-03", "title": "Poor Lead Data Quality",
        "severity": "Medium", "probability": "Medium",
        "status": "Monitoring",
        "mitigation": "Pilot scoped to inbound leads only. Dormant list audit scheduled for Week 4.",
    },
    {
        "id": "R-04", "title": "Unclear Escalation Rules",
        "severity": "High", "probability": "Low",
        "status": "Mitigated",
        "mitigation": "Escalation playbook drafted and in client review. Sign-off expected by Week 4.",
    },
    {
        "id": "R-05", "title": "Stakeholder Misalignment (Ops vs IT vs Clinical)",
        "severity": "Medium", "probability": "Medium",
        "status": "Monitoring",
        "mitigation": "Single DRI confirmed (VP Operations). Weekly check-in cadence established.",
    },
    {
        "id": "R-06", "title": "Low Agent Response Quality",
        "severity": "High", "probability": "Low",
        "status": "Monitoring",
        "mitigation": "Confidence threshold + escalation fallback built into design. Red-team QA planned.",
    },
]

OPEN_ITEMS = [
    {"item": "EHR sandbox credentials", "owner": "Client IT", "due": "2026-04-20", "blocker": True},
    {"item": "BAA execution", "owner": "Client Legal", "due": "2026-04-21", "blocker": True},
    {"item": "Escalation routing sign-off", "owner": "Client Clinical Ops", "due": "2026-04-25", "blocker": False},
    {"item": "FAQ document from clinical team", "owner": "Client Clinical Ops", "due": "2026-04-23", "blocker": False},
    {"item": "Confirm pilot provider cohort (2 names)", "owner": "Client Ops", "due": "2026-04-28", "blocker": False},
]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

STATUS_COLOR = {
    "Complete":    "#2ecc71",
    "In Progress": "#f39c12",
    "Blocked":     "#e74c3c",
    "Not Started": "#95a1ac",
    "At Risk":     "#e74c3c",
    "Done":        "#2ecc71",
    "Upcoming":    "#95a1ac",
    "Mitigated":   "#2ecc71",
    "Monitoring":  "#f39c12",
    "Active":      "#e74c3c",
}

RAG_COLOR = {"GREEN": "#2ecc71", "AMBER": "#f39c12", "RED": "#e74c3c"}

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


def status_badge(label):
    color = STATUS_COLOR.get(label, "#95a1ac")
    return f'<span style="background:{color};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;white-space:nowrap;display:inline-block">{label}</span>'


def pct_bar(pct, status):
    color = STATUS_COLOR.get(status, "#95a1ac")
    return f"""
    <div style="background:#eee;border-radius:6px;height:14px;width:100%">
      <div style="background:{color};width:{pct}%;height:14px;border-radius:6px;transition:width 0.3s"></div>
    </div>
    <small style="color:#666">{pct}%</small>
    """


# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Launch Readiness Tracker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init (run once) ─────────────
if "eng" not in st.session_state:
    st.session_state.eng = ENGAGEMENT.copy()
if "ws" not in st.session_state:
    st.session_state.ws = [w.copy() for w in WORKSTREAMS]
if "lc" not in st.session_state:
    st.session_state.lc = list(LAUNCH_CRITERIA)
if "risks" not in st.session_state:
    st.session_state.risks = [r.copy() for r in RISKS]
if "items" not in st.session_state:
    st.session_state["items"] = [i.copy() for i in OPEN_ITEMS]

# Shortcuts
eng   = st.session_state.eng
ws    = st.session_state.ws
lc    = st.session_state.lc
risks = st.session_state.risks
items = st.session_state["items"]

# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown("### Engagement")
    st.markdown(f"**{eng['name']}**")
    st.markdown(f"Client: `{eng['client']}`")
    st.markdown(f"Delivery Lead: {eng['delivery_lead']}")
    st.divider()

    st.markdown(f"**Week {eng['current_week']} of {eng['total_weeks']}**")
    st.progress(eng["current_week"] / eng["total_weeks"])
    st.divider()

    # ── Edit Mode ─────────────────────────────
    edit_mode = st.toggle("✏️ Edit Mode", value=False)

    if edit_mode:
        st.markdown("**Overall**")
        eng["overall_status"] = st.selectbox(
            "Delivery Status", ["GREEN", "AMBER", "RED"],
            index=["GREEN", "AMBER", "RED"].index(eng["overall_status"]),
            key="rag_select"
        )
        eng["current_week"] = st.slider(
            "Current Week", 1, eng["total_weeks"], eng["current_week"]
        )
        eng["status_note"] = st.text_area(
            "Status Note", eng["status_note"], height=80
        )
        st.divider()

        st.markdown("**Workstreams**")
        for i, w in enumerate(ws):
            with st.expander(f"{w['id']}"):
                w["status"] = st.selectbox(
                    "Status", ["Complete", "In Progress", "Blocked", "At Risk", "Not Started"],
                    index=["Complete", "In Progress", "Blocked", "At Risk", "Not Started"].index(w["status"]),
                    key=f"ws_status_{i}"
                )
                w["pct"] = st.slider("Completion %", 0, 100, w["pct"], key=f"ws_pct_{i}")
                w["note"] = st.text_input("Note", w["note"], key=f"ws_note_{i}")
        st.divider()

        st.markdown("**Launch Criteria**")
        status_map = {True: "Pass", False: "Fail", None: "Not Tested"}
        reverse_map = {"Pass": True, "Fail": False, "Not Tested": None}
        new_lc = []
        for i, (criterion, owner, s) in enumerate(lc):
            val = st.selectbox(
                criterion[:40] + "…" if len(criterion) > 40 else criterion,
                ["Pass", "Fail", "Not Tested"],
                index=["Pass", "Fail", "Not Tested"].index(status_map[s]),
                key=f"lc_{i}"
            )
            new_lc.append((criterion, owner, reverse_map[val]))
        st.session_state.lc = new_lc
        lc = st.session_state.lc
        st.divider()

        st.markdown("**Risks**")
        for i, r in enumerate(risks):
            with st.expander(r["id"]):
                r["status"] = st.selectbox(
                    "Status", ["Active", "Monitoring", "Mitigated"],
                    index=["Active", "Monitoring", "Mitigated"].index(r["status"]),
                    key=f"risk_{i}"
                )
        st.divider()

        st.markdown("**Open Items**")
        for i, item in enumerate(items):
            item["blocker"] = st.checkbox(
                f"🔴 {item['item']}" if item["blocker"] else f"🟡 {item['item']}",
                value=item["blocker"], key=f"item_{i}"
            )
        st.divider()

        if st.button("Reset to defaults", use_container_width=True):
            for key in ["eng", "ws", "lc", "risks", "items"]:
                del st.session_state[key]
            st.rerun()

    # ── Directives viewer ─────────────────────
    st.markdown("**Directives**")
    st.caption("Click to preview SOP content")
    for w in ws:
        with st.expander(f"{w['id']} — {w['name']}"):
            st.caption(f"📄 `{w['directive']}`")
            st.markdown("**Done when:**")
            for criterion in w["done_when"]:
                st.markdown(f"- {criterion}")
            try:
                content = open(w["directive"]).read()
                if st.button("Show full directive", key=f"dir_{w['id']}"):
                    st.markdown(content)
            except FileNotFoundError:
                st.caption("File not found — check path")

    st.divider()
    st.caption(f"Last updated: {date.today()}")

# ── Header ───────────────────────────────────
rag       = eng["overall_status"]
rag_color = RAG_COLOR[rag]

st.title("🏥 Launch Readiness Tracker")
st.markdown(f"*{eng['name']} — {eng['client']}*")

col_rag, col_guide, col_ws = st.columns([1, 2, 2], gap="medium")

with col_rag:
    st.markdown(f"""
    <div style="background:{rag_color};color:white;text-align:center;
                padding:18px 14px;border-radius:10px;">
      <div style="font-size:11px;font-weight:600;letter-spacing:1px">DELIVERY STATUS</div>
      <div style="font-size:28px;font-weight:700;margin:6px 0">{rag}</div>
      <div style="font-size:11px;line-height:1.5;opacity:0.92">{eng['status_note']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_guide:
    st.markdown(f"""
    <div style="border:1.5px solid #ddd;border-radius:10px;padding:14px 16px;height:100%">
      <div style="font-size:12px;font-weight:700;letter-spacing:0.5px;color:#444;margin-bottom:10px">
        OVERALL STATUS GUIDE
      </div>
      <div style="margin-bottom:6px">
        <span style="color:#2ecc71;font-weight:700">● GREEN</span>
        <span style="font-size:12px;color:#555"> — All workstreams on schedule, no active blockers</span>
      </div>
      <div style="margin-bottom:6px">
        <span style="color:#f39c12;font-weight:700">● AMBER</span>
        <span style="font-size:12px;color:#555"> — 1–2 risks active, being managed, pilot date at risk</span>
      </div>
      <div>
        <span style="color:#e74c3c;font-weight:700">● RED</span>
        <span style="font-size:12px;color:#555"> — Critical blocker, compliance issue, or go-live threatened</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_ws:
    st.markdown(f"""
    <div style="border:1.5px solid #ddd;border-radius:10px;padding:14px 16px;height:100%">
      <div style="font-size:12px;font-weight:700;letter-spacing:0.5px;color:#444;margin-bottom:10px">
        WORKSTREAM STATUS GUIDE
      </div>
      <div style="margin-bottom:5px;font-size:12px;color:#555">✅ <b>Complete</b> — All outputs delivered &amp; signed off</div>
      <div style="margin-bottom:5px;font-size:12px;color:#555">🔵 <b>In Progress</b> — Active work underway, on schedule</div>
      <div style="margin-bottom:5px;font-size:12px;color:#555">🔴 <b>Blocked</b> — Cannot proceed, dependency unresolved</div>
      <div style="margin-bottom:5px;font-size:12px;color:#555">⚠️ <b>At Risk</b> — Behind schedule or dependency unclear</div>
      <div style="font-size:12px;color:#555">⬜ <b>Not Started</b> — Scheduled for a future week</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.info(f"**Status Note:** {eng['status_note']}")
st.divider()

# ── Layout: tabs (left) + insights panel (right) ─────
col_main, col_right = st.columns([3, 2], gap="large")

# ── Insights Panel ────────────────────────────
with col_right:
    st.markdown("### 🤖 Delivery Insights")
    st.caption("AI analysis of current workstream state")

    if st.button("Generate Delivery Insights", type="primary", use_container_width=True):
        with st.spinner("Analyzing engagement data..."):
            raw, source = generate_insights(
                eng, ws, risks, items, lc
            )
            st.session_state["insights"] = raw
            st.session_state["insights_source"] = source

    if "insights" in st.session_state:
        parsed = parse_insights(st.session_state["insights"])
        source = st.session_state.get("insights_source", "")

        st.markdown("---")
        st.markdown("**Project Summary**")
        st.info(parsed["summary"])

        st.markdown("**Key Risks Right Now**")
        st.warning(parsed["risks"])

        st.markdown("**Recommended Next Actions**")
        st.success(parsed["actions"])

        st.caption(f"Generated by: {source}")

# ── Tabs (main column) ────────────────────────
with col_main:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Workstream Health",
        "✅ Launch Criteria",
        "⚠️ Risk Register",
        "🗓️ Milestones",
        "🚧 Open Items",
    ])

    with tab1:
        st.subheader("Workstream Health")

        blocked = sum(1 for w in ws if w["status"] == "Blocked")
        complete = sum(1 for w in ws if w["status"] == "Complete")
        in_progress = sum(1 for w in ws if w["status"] == "In Progress")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Workstreams Complete", f"{complete} / {len(ws)}")
        m2.metric("In Progress", in_progress)
        m3.metric("Blocked", blocked, delta=f"-{blocked} need action" if blocked else None,
                  delta_color="inverse")
        avg_pct = sum(w["pct"] for w in ws) // len(ws)
        m4.metric("Avg Completion", f"{avg_pct}%")

        st.divider()

        for w in ws:
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 3, 2, 4])
                with c1:
                    st.markdown(f"**{w['id']}**")
                    st.markdown(status_badge(w["status"]), unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{w['name']}**")
                    st.caption(f"Owner: {w['owner']}")
                with c3:
                    st.markdown(pct_bar(w["pct"], w["status"]), unsafe_allow_html=True)
                    st.caption(f"Weeks {w['weeks']}")
                with c4:
                    st.caption(w["note"])

                with st.expander(f"What does 100% mean for {w['id']}?"):
                    for item in w["done_when"]:
                        done = w["pct"] == 100
                        icon = "✅" if done else ("🔴" if w["status"] == "Blocked" else "⏳")
                        st.markdown(f"{icon} {item}")
            st.divider()

    with tab2:
        st.subheader("Launch Criteria Checklist")
        st.caption("Sourced from: directives/ws5_qa_pilot_readiness.md — all items must be green before pilot go-live.")

        passed = sum(1 for _, _, s in lc if s is True)
        failed = sum(1 for _, _, s in lc if s is False)
        pending = sum(1 for _, _, s in lc if s is None)

        c1, c2, c3 = st.columns(3)
        c1.metric("✅ Pass", passed)
        c2.metric("❌ Fail / Blocked", failed)
        c3.metric("⏳ Not Yet Tested", pending)

        if failed > 0:
            st.error(f"{failed} criteria currently failing — pilot go-live is blocked.")
        elif pending == 0:
            st.success("All criteria passed — ready for go/no-go decision.")
        else:
            st.warning(f"{pending} criteria not yet tested. Pilot date depends on WS-3 and WS-4 completion.")

        st.divider()

        for criterion, owner, status in lc:
            col_icon, col_text, col_owner = st.columns([1, 5, 3])
            if status is True:
                icon, color = "✅", "#2ecc71"
            elif status is False:
                icon, color = "❌", "#e74c3c"
            else:
                icon, color = "⏳", "#95a1ac"
            with col_icon:
                st.markdown(f"<span style='font-size:20px'>{icon}</span>", unsafe_allow_html=True)
            with col_text:
                st.markdown(f"<span style='color:{color}'>{criterion}</span>", unsafe_allow_html=True)
            with col_owner:
                st.caption(f"Owner: {owner}")

    with tab3:
        st.subheader("Risk Register")
        st.caption("Sourced from: docs/01_delivery_operating_model.md — Risk View section.")

        sorted_risks = sorted(risks, key=lambda r: (SEVERITY_ORDER.get(r["severity"], 9),
                                                       0 if r["status"] == "Active" else 1))

        for r in sorted_risks:
            sev_color = {"Critical": "#e74c3c", "High": "#e67e22", "Medium": "#f39c12", "Low": "#27ae60"}.get(r["severity"], "#999")

            with st.expander(f"{r['id']} — {r['title']}"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Severity:** <span style='color:{sev_color};font-weight:700'>{r['severity']}</span>", unsafe_allow_html=True)
                c2.markdown(f"**Probability:** {r['probability']}")
                c3.markdown(status_badge(r["status"]), unsafe_allow_html=True)
                st.markdown(f"**Mitigation:** {r['mitigation']}")

    with tab4:
        st.subheader("Milestone Timeline — Weeks 1–8")

        current_week = eng["current_week"]

        for m in MILESTONES:
            week = m["week"]
            is_current = week == current_week
            col_week, col_status, col_name = st.columns([1, 2, 6])
            with col_week:
                label = f"**W{week}**" if is_current else f"W{week}"
                st.markdown(f"{'🔵 ' if is_current else ''}{label}")
            with col_status:
                st.markdown(status_badge(m["status"]), unsafe_allow_html=True)
            with col_name:
                st.markdown(m["milestone"])

    with tab5:
        st.subheader("Open Items & Decisions Needed")

        blockers = [i for i in items if i["blocker"]]
        non_blockers = [i for i in items if not i["blocker"]]

        if blockers:
            st.error(f"🚨 {len(blockers)} active blocker(s) — immediate action required")
            for item in blockers:
                with st.container():
                    c1, c2, c3 = st.columns([4, 2, 2])
                    c1.markdown(f"🔴 **{item['item']}**")
                    c2.markdown(f"Owner: **{item['owner']}**")
                    c3.markdown(f"Due: **{item['due']}**")

        st.divider()

        if non_blockers:
            st.warning("Pending items (not blocking)")
            for item in non_blockers:
                with st.container():
                    c1, c2, c3 = st.columns([4, 2, 2])
                    c1.markdown(f"🟡 {item['item']}")
                    c2.caption(f"Owner: {item['owner']}")
                    c3.caption(f"Due: {item['due']}")
