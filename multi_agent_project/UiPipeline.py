import streamlit as st
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #09090f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #09090f; }
::-webkit-scrollbar-thumb { background: #3a3a5c; border-radius: 4px; }

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #7c6af5;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 30%, #9f8fff 70%, #6c4ef5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.6rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6e6b88;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Input Card ── */
.input-card {
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem auto;
    max-width: 780px;
    box-shadow: 0 0 60px rgba(108, 78, 245, 0.06);
}

[data-testid="stTextInput"] input {
    background: #0a0a14 !important;
    border: 1px solid #2a2a42 !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #6c4ef5 !important;
    box-shadow: 0 0 0 3px rgba(108, 78, 245, 0.15) !important;
}
[data-testid="stTextInput"] label {
    color: #9b98b8 !important;
    font-size: 0.8rem !important;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: 0.05em !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6c4ef5 0%, #9f6af5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100% !important;
    box-shadow: 0 4px 24px rgba(108, 78, 245, 0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(108, 78, 245, 0.5) !important;
}

/* ── Global Progress Bar ── */
.global-progress-wrap {
    margin: 1.5rem 0 0.5rem;
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
}
.progress-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6c4ef5;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.progress-track {
    background: #1a1a28;
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
    position: relative;
}
.progress-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #6c4ef5, #9f6af5, #c084fc);
    background-size: 200% 100%;
    animation: shimmer 1.8s linear infinite;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes shimmer {
    0%   { background-position: 200% center; }
    100% { background-position: -200% center; }
}
.progress-pct {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #5a5875;
    text-align: right;
    margin-top: 0.4rem;
}

/* ── Step Cards ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.step-card {
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 1.4rem 1rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.step-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(108,78,245,0.08) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.4s;
}
.step-card.active::after { opacity: 1; }

.step-card.active {
    border-color: #6c4ef5;
    background: #13101f;
    box-shadow: 0 0 0 1px rgba(108,78,245,0.3), 0 8px 32px rgba(108, 78, 245, 0.25);
    transform: translateY(-2px);
}
.step-card.done {
    border-color: #2dd4a0;
    background: #0e1a16;
    box-shadow: 0 0 16px rgba(45, 212, 160, 0.12);
}
.step-card.idle {
    opacity: 0.45;
}
.step-icon {
    font-size: 1.6rem;
    margin-bottom: 0.6rem;
    transition: transform 0.3s;
    display: block;
}
.step-card.active .step-icon {
    animation: bob 1.2s ease-in-out infinite;
}
@keyframes bob {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-4px); }
}
.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #3e3c58;
    margin-bottom: 0.4rem;
    transition: color 0.3s;
}
.step-card.active .step-label { color: #9f8fff; }
.step-card.done  .step-label  { color: #2dd4a0; }
.step-sublabel {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: #2e2c44;
    min-height: 1rem;
    transition: color 0.3s;
}
.step-card.active .step-sublabel { color: #6c4ef5; }
.step-card.done  .step-sublabel  { color: #1a6e55; }

/* Spinner ring inside active card */
.spin-ring {
    display: inline-block;
    width: 18px; height: 18px;
    border: 2px solid rgba(108,78,245,0.2);
    border-top-color: #6c4ef5;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 0.4rem;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
.check-mark {
    display: inline-block;
    width: 18px; height: 18px;
    background: #2dd4a0;
    border-radius: 50%;
    line-height: 18px;
    font-size: 0.7rem;
    color: #09090f;
    margin-bottom: 0.4rem;
    font-weight: 700;
}

/* ── Current task description ── */
.task-description {
    background: #0e0e1a;
    border: 1px solid #1e1e30;
    border-left: 3px solid #6c4ef5;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0 1.2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: #9f8fff;
    display: flex;
    align-items: center;
    gap: 0.7rem;
    animation: fadeSlide 0.3s ease;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateX(-6px); }
    to   { opacity: 1; transform: translateX(0); }
}
.task-description .task-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #6c4ef5;
    flex-shrink: 0;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(108,78,245,0.4); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 5px rgba(108,78,245,0); }
}

/* ── Log Console ── */
.log-console {
    background: #06060d;
    border: 1px solid #1a1a28;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.73rem;
    color: #4a4760;
    line-height: 2;
    max-height: 200px;
    overflow-y: auto;
    margin: 1rem 0;
    position: relative;
}
.log-console::before {
    content: 'PIPELINE LOG';
    position: absolute;
    top: 0.7rem; right: 1rem;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: #1e1e30;
}
.log-line { margin: 0; }
.log-line.info { color: #6c4ef5; }
.log-line.ok   { color: #2dd4a0; }
.log-line.warn { color: #f59e0b; }
.log-timestamp { color: #2a2a3a; margin-right: 0.8rem; }

/* ── Result Sections ── */
.result-section {
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin: 1.2rem 0;
    position: relative;
    animation: fadeUp 0.4s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-section::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
}
.result-section.search::before { background: #6c4ef5; }
.result-section.scrape::before { background: #f59e0b; }
.result-section.report::before { background: #3b82f6; }
.result-section.critic::before { background: #2dd4a0; }

.section-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 6px;
    font-weight: 500;
}
.badge-search { background: rgba(108,78,245,0.15); color: #9f8fff; }
.badge-scrape { background: rgba(245,158,11,0.15); color: #fbbf24; }
.badge-report { background: rgba(59,130,246,0.15); color: #60a5fa; }
.badge-critic { background: rgba(45,212,160,0.15); color: #34d399; }

.section-content {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    line-height: 1.8;
    color: #b0adc8;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
    padding-right: 0.5rem;
    margin-top: 0.8rem;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #1a1a28;
    border-radius: 99px;
    padding: 0.3rem 0.9rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #5a5875;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
}
.status-pill.running { color: #9f8fff; background: rgba(108,78,245,0.12); }
.status-pill.done    { color: #2dd4a0; background: rgba(45,212,160,0.1); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; animation: pulse 1.2s infinite; }
.status-pill.done .dot { animation: none; }

/* ── Divider ── */
.fancy-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a42 50%, transparent);
    margin: 2rem 0;
}

/* ── Error ── */
.error-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    color: #f87171;
    font-size: 0.85rem;
    font-family: 'DM Mono', monospace;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #2e2c44;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.empty-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

[data-testid="stExpander"] {
    background: #111118 !important;
    border: 1px solid #1e1e30 !important;
    border-radius: 12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero-wrap">
    <div class="hero-eyebrow">Multi-Agent Research System</div>
    <h1 class="hero-title">Deep Research<br>On Autopilot</h1>
    <p class="hero-sub">Four specialized AI agents — Search · Scrape · Write · Critique — working in concert to produce rigorous, structured reports.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Step definitions ──────────────────────────────────────────────────────────
STEPS = [
    {
        "key": "search",
        "icon": "🔍",
        "label": "Search Agent",
        "active_sub": "Querying the web…",
        "done_sub": "Results captured",
        "task_msg": "Search Agent is scouring the web for the most relevant and recent sources on your topic.",
    },
    {
        "key": "reader",
        "icon": "📄",
        "label": "Reader Agent",
        "active_sub": "Scraping content…",
        "done_sub": "Content extracted",
        "task_msg": "Reader Agent is visiting the top URL and extracting deep content from the page.",
    },
    {
        "key": "writer",
        "icon": "✍️",
        "label": "Writer Chain",
        "active_sub": "Drafting report…",
        "done_sub": "Draft ready",
        "task_msg": "Writer Chain is synthesising all gathered information into a structured, coherent report.",
    },
    {
        "key": "critic",
        "icon": "🧐",
        "label": "Critic Chain",
        "active_sub": "Reviewing…",
        "done_sub": "Review complete",
        "task_msg": "Critic Chain is carefully reviewing the report for accuracy, gaps, and quality.",
    },
]

STEP_PROGRESS = {"search": 25, "reader": 50, "writer": 75, "critic": 100}


# ── Helpers ───────────────────────────────────────────────────────────────────
def render_step_cards(active_step=None, done_steps=None):
    done_steps = done_steps or []
    cards_html = '<div class="pipeline-grid">'
    for s in STEPS:
        key = s["key"]
        if key in done_steps:
            cls = "step-card done"
            indicator = f'<span class="check-mark">✓</span>'
            sub = s["done_sub"]
        elif key == active_step:
            cls = "step-card active"
            indicator = '<span class="spin-ring"></span>'
            sub = s["active_sub"]
        else:
            cls = "step-card idle"
            indicator = f'<span class="step-icon">{s["icon"]}</span>'
            sub = "—"

        if key in done_steps or key == active_step:
            cards_html += f"""
            <div class="{cls}">
                {indicator}
                <div class="step-label">{s['label']}</div>
                <div class="step-sublabel">{sub}</div>
            </div>"""
        else:
            cards_html += f"""
            <div class="{cls}">
                <span class="step-icon">{s['icon']}</span>
                <div class="step-label">{s['label']}</div>
                <div class="step-sublabel">{sub}</div>
            </div>"""
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)


def render_progress_bar(active_step, done_steps):
    pct = 0
    if active_step:
        pct = STEP_PROGRESS.get(active_step, 0)
    elif done_steps:
        pct = STEP_PROGRESS.get(done_steps[-1], 0)

    active_step_data = next((s for s in STEPS if s["key"] == active_step), None)
    label = active_step_data["label"] if active_step_data else "Pipeline complete"

    st.markdown(
        f"""
    <div class="global-progress-wrap">
        <div class="progress-label">
            <span>{'⚙ ' if active_step else '✓ '}{label}</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width:{pct}%;{'animation: none;' if not active_step else ''}"></div>
        </div>
        <div class="progress-pct">{pct}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_task_description(active_step):
    step_data = next((s for s in STEPS if s["key"] == active_step), None)
    if step_data:
        st.markdown(
            f"""
        <div class="task-description">
            <span class="task-dot"></span>
            {step_data['task_msg']}
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_logs(logs):
    if not logs:
        return
    lines = []
    for i, (cls, msg) in enumerate(logs):
        tag = "INFO" if cls == "info" else "OK  " if cls == "ok" else "WARN"
        ts = f"[{i+1:02d}]"
        lines.append(
            f'<p class="log-line {cls}"><span class="log-timestamp">{ts}</span>[{tag}]  {msg}</p>'
        )
    log_html = "\n".join(lines)
    st.markdown(f'<div class="log-console">{log_html}</div>', unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
topic_input = st.text_input(
    "RESEARCH TOPIC",
    placeholder="e.g. Recent advances in quantum error correction",
    key="topic",
)
run_btn = st.button("⚡  Run Pipeline", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [
    ("results", {}),
    ("running", False),
    ("logs", []),
    ("active_step", None),
    ("done_steps", []),
    ("error", None),
    ("pipeline_step", None),  # which step to execute on next render
    ("pipeline_topic", ""),  # topic carried across reruns
    ("pipeline_state", {}),  # intermediate data between steps
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Step executor — runs exactly ONE step then stops ─────────────────────────
def execute_current_step():
    """Called once per rerun while pipeline is running. Executes one step."""
    step = st.session_state.pipeline_step
    topic = st.session_state.pipeline_topic
    state = st.session_state.pipeline_state

    try:
        from agents import (
            critic_chain,
            writer_chain,
            build_search_agent,
            build_reader_agent,
        )

        # ── Step 1: Search ────────────────────────────────────────────────────
        if step == "search":
            st.session_state.active_step = "search"
            st.session_state.logs.append(
                ("info", "Search Agent initialised — querying the web…")
            )

            search_agent = build_search_agent()
            result = search_agent.invoke(
                {
                    "messages": [
                        f"Find recent, reliable and detailed information about: {topic}"
                    ]
                }
            )
            state["Search_result"] = result["messages"][-1].content
            st.session_state.results["search"] = state["Search_result"]
            st.session_state.done_steps.append("search")
            st.session_state.logs.append(("ok", "Search complete — results captured."))
            st.session_state.pipeline_step = "reader"  # queue next step

        # ── Step 2: Reader ────────────────────────────────────────────────────
        elif step == "reader":
            st.session_state.active_step = "reader"
            st.session_state.logs.append(
                ("warn", "Reader Agent selecting and scraping top URL…")
            )

            reader_agent = build_reader_agent()
            result = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"Based on the following search results about {topic}, "
                            f"pick the most relevant url and scrape it for deeper content. "
                            f"Search results: {state['Search_result'][:800]}",
                        )
                    ]
                }
            )
            state["Scraped_content"] = result["messages"][-1].content
            st.session_state.results["scrape"] = state["Scraped_content"]
            st.session_state.done_steps.append("reader")
            st.session_state.logs.append(
                ("ok", "Scraping complete — content extracted.")
            )
            st.session_state.pipeline_step = "writer"

        # ── Step 3: Writer ────────────────────────────────────────────────────
        elif step == "writer":
            st.session_state.active_step = "writer"
            st.session_state.logs.append(
                ("info", "Writer Chain synthesising and drafting report…")
            )

            combined = (
                f"Search Results: {state['Search_result']}\n"
                f"Detailed Scraped Content: {state['Scraped_content']}"
            )
            state["report"] = writer_chain.invoke(
                {"topic": topic, "research": combined}
            )
            st.session_state.results["report"] = state["report"]
            st.session_state.done_steps.append("writer")
            st.session_state.logs.append(("ok", "Draft report ready."))
            st.session_state.pipeline_step = "critic"

        # ── Step 4: Critic ────────────────────────────────────────────────────
        elif step == "critic":
            st.session_state.active_step = "critic"
            st.session_state.logs.append(
                ("warn", "Critic Chain reviewing the draft report…")
            )

            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            st.session_state.results["critic"] = state["feedback"]
            st.session_state.done_steps.append("critic")
            st.session_state.logs.append(("ok", "Review complete. Pipeline finished ✓"))

            # Pipeline done
            st.session_state.active_step = None
            st.session_state.pipeline_step = None
            st.session_state.running = False

        # Persist intermediate state back
        st.session_state.pipeline_state = state

    except Exception as exc:
        st.session_state.error = str(exc)
        st.session_state.logs.append(("warn", f"Error: {exc}"))
        st.session_state.active_step = None
        st.session_state.pipeline_step = None
        st.session_state.running = False


# ── Trigger ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic_input.strip():
        st.warning("Please enter a research topic first.")
    else:
        # Reset everything and kick off with first step queued
        st.session_state.results = {}
        st.session_state.logs = []
        st.session_state.done_steps = []
        st.session_state.active_step = "search"  # show immediately on next render
        st.session_state.error = None
        st.session_state.running = True
        st.session_state.pipeline_step = "search"
        st.session_state.pipeline_topic = topic_input.strip()
        st.session_state.pipeline_state = {}
        st.rerun()  # ← page re-renders showing "search" as active BEFORE any work

# ── Status pill ───────────────────────────────────────────────────────────────
if st.session_state.running:
    st.markdown(
        '<div class="status-pill running"><span class="dot"></span>Pipeline running…</div>',
        unsafe_allow_html=True,
    )
elif st.session_state.results:
    st.markdown(
        '<div class="status-pill done"><span class="dot"></span>Pipeline complete</div>',
        unsafe_allow_html=True,
    )

# ── Progress bar + Step cards ─────────────────────────────────────────────────
if st.session_state.running or st.session_state.results or st.session_state.error:
    render_progress_bar(
        active_step=st.session_state.active_step,
        done_steps=st.session_state.done_steps,
    )
    render_step_cards(
        active_step=st.session_state.active_step,
        done_steps=st.session_state.done_steps,
    )
    if st.session_state.active_step:
        render_task_description(st.session_state.active_step)

# ── Log console ───────────────────────────────────────────────────────────────
render_logs(st.session_state.logs)

# ── Error ─────────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="error-box">⚠ {st.session_state.error}</div>',
        unsafe_allow_html=True,
    )

# ── Results ───────────────────────────────────────────────────────────────────
results = st.session_state.results

if results:
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown(
        """
    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                color:#e8e6f0;margin-bottom:1.2rem;">Research Output</div>
    """,
        unsafe_allow_html=True,
    )

    if "search" in results:
        st.markdown(
            """
        <div class="result-section search">
            <span class="section-badge badge-search">🔍 Search Agent</span>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="section-content">{results["search"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if "scrape" in results:
        st.markdown(
            """
        <div class="result-section scrape">
            <span class="section-badge badge-scrape">📄 Reader Agent</span>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="section-content">{results["scrape"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if "report" in results:
        st.markdown(
            """
        <div class="result-section report">
            <span class="section-badge badge-report">✍️ Writer Chain — Final Report</span>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="section-content">{results["report"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Report (.txt)",
            data=results["report"],
            file_name=f"report_{topic_input[:30].replace(' ', '_')}.txt",
            mime="text/plain",
        )

    if "critic" in results:
        st.markdown(
            """
        <div class="result-section critic">
            <span class="section-badge badge-critic">🧐 Critic Chain — Review</span>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="section-content">{results["critic"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.running and not results and not st.session_state.error:
    render_step_cards()
    st.markdown(
        """
    <div class="empty-state">
        <div class="empty-icon">🔬</div>
        <div class="empty-text">Enter a topic above to begin</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ── Execute next pipeline step (AFTER full UI has rendered above) ─────────────
# This is placed at the very end so Streamlit flushes the UI first,
# then runs the agent work, then st.rerun() triggers a fresh render.
if st.session_state.running and st.session_state.pipeline_step:
    execute_current_step()
    st.rerun()
