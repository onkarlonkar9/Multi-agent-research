import streamlit as st
import sys, os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Helper: safely extract string from any agent return value ─────────────────
def extract_content(value) -> str:
    """Convert whatever LangChain returns into a plain string."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif hasattr(item, "content"):
                parts.append(str(item.content))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if hasattr(value, "content"):
        return str(value.content)
    return str(value)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --bg:        #05070d;
    --s1:        #0c0f1a;
    --s2:        #111627;
    --border:    #1c2240;
    --cyan:      #00f5d4;
    --pink:      #f72585;
    --orange:    #ff6b35;
    --yellow:    #ffd60a;
    --purple:    #7b2fff;
    --blue:      #4cc9f0;
    --text:      #e8eaf6;
    --muted:     #546e7a;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    font-family: 'Exo 2', sans-serif;
    color: var(--text);
}

[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMainBlockContainer"] { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem 4rem; }

/* ══ HERO ══════════════════════════════════════════════════════════════════ */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 40% at 20% 50%, rgba(0,245,212,.08) 0%, transparent 70%),
        radial-gradient(ellipse 50% 35% at 80% 40%, rgba(123,47,255,.1) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 50% 0%,  rgba(247,37,133,.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--cyan);
    border: 1px solid rgba(0,245,212,.35);
    border-radius: 999px;
    padding: 5px 14px;
    margin-bottom: 1.4rem;
    background: rgba(0,245,212,.06);
}
.hero-pill span {
    width:6px;height:6px;border-radius:50%;
    background:var(--cyan);animation:pulse 1.6s infinite;
}
@keyframes pulse {
    0%,100%{opacity:1;transform:scale(1)}
    50%{opacity:.4;transform:scale(.7)}
}
.hero-title {
    font-size: clamp(2.2rem, 6vw, 4rem);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}
.hero-title .w1 { color: var(--cyan); }
.hero-title .w2 { color: var(--text); }
.hero-title .w3 {
    background: linear-gradient(90deg, var(--pink), var(--orange));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-size: 1rem; color: var(--muted); max-width: 500px; margin: 0 auto; line-height: 1.6; }

/* ══ INPUT ════════════════════════════════════════════════════════════════ */
.input-shell {
    background: linear-gradient(135deg, rgba(0,245,212,.04), rgba(123,47,255,.06));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem 2rem 1.5rem;
    margin: 1.5rem 0;
    position: relative;
}
.input-shell::before {
    content: '';
    position: absolute;
    top: -1px; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--purple), transparent);
}
.input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 0.7rem;
}
.stTextInput > div > div > input {
    background: rgba(0,0,0,.4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.8rem 1.1rem !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(0,245,212,.12) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: 0.8rem !important; }

.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--cyan), var(--purple)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.78rem 1.5rem !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button:hover  { opacity: .85 !important; transform: translateY(-2px) !important; }
.stButton > button:disabled {
    background: var(--s2) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
}

/* ══ STEPS ════════════════════════════════════════════════════════════════ */
.steps-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 1.8rem 0 1.2rem; }
.step-box {
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1rem 1.1rem;
    text-align: center;
    background: var(--s1);
    position: relative;
    overflow: hidden;
    transition: border-color .3s, box-shadow .3s;
}
.step-box.waiting { opacity: .38; }
.step-box.active  { animation: stepPulse 1.8s ease-in-out infinite; }

.step-box.done-0  { border-color: var(--cyan);   box-shadow: 0 0 22px rgba(0,245,212,.2); }
.step-box.done-1  { border-color: var(--blue);   box-shadow: 0 0 22px rgba(76,201,240,.2); }
.step-box.done-2  { border-color: var(--purple); box-shadow: 0 0 22px rgba(123,47,255,.2); }
.step-box.done-3  { border-color: var(--pink);   box-shadow: 0 0 22px rgba(247,37,133,.2); }
.step-box.active-0{ border-color: var(--cyan); }
.step-box.active-1{ border-color: var(--blue); }
.step-box.active-2{ border-color: var(--purple); }
.step-box.active-3{ border-color: var(--pink); }

.step-box.done-0::after { content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at 50% 0%, rgba(0,245,212,.09), transparent 70%); }
.step-box.done-1::after { content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at 50% 0%, rgba(76,201,240,.09), transparent 70%); }
.step-box.done-2::after { content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at 50% 0%, rgba(123,47,255,.11), transparent 70%); }
.step-box.done-3::after { content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at 50% 0%, rgba(247,37,133,.09), transparent 70%); }

@keyframes stepPulse { 0%,100%{ box-shadow:none; } 50%{ box-shadow: 0 0 28px rgba(255,255,255,.12); } }

.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; letter-spacing:.15em; text-transform:uppercase; margin-bottom:6px;
}
.step-box.waiting .step-num  { color: var(--muted); }
.step-box.done-0  .step-num,
.step-box.active-0 .step-num { color: var(--cyan); }
.step-box.done-1  .step-num,
.step-box.active-1 .step-num { color: var(--blue); }
.step-box.done-2  .step-num,
.step-box.active-2 .step-num { color: var(--purple); }
.step-box.done-3  .step-num,
.step-box.active-3 .step-num { color: var(--pink); }

.step-icon { font-size: 1.75rem; margin-bottom: 5px; }
.step-name { font-weight: 700; font-size: 0.88rem; }
.step-sub  { font-size:.72rem; color:var(--muted); margin-top:3px; }
.step-tick { font-size: 1.1rem; margin-top: 4px; }

/* ══ RESULT PANELS ════════════════════════════════════════════════════════ */
.rp {
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.rp::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: 14px 14px 0 0;
}
.rp-search { background: linear-gradient(135deg,rgba(0,245,212,.05),transparent); }
.rp-search::before { background: linear-gradient(90deg, var(--cyan), var(--blue)); }
.rp-scrape { background: linear-gradient(135deg,rgba(76,201,240,.05),transparent); }
.rp-scrape::before { background: linear-gradient(90deg, var(--blue), var(--purple)); }
.rp-report { background: linear-gradient(135deg,rgba(123,47,255,.07),transparent); }
.rp-report::before { background: linear-gradient(90deg, var(--purple), var(--pink)); }
.rp-critic { background: linear-gradient(135deg,rgba(247,37,133,.06),transparent); }
.rp-critic::before { background: linear-gradient(90deg, var(--pink), var(--orange)); }

.rp-head { display:flex; align-items:center; gap:10px; margin-bottom:1rem; }
.rp-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.rp-search .rp-dot { background: var(--cyan); }
.rp-scrape .rp-dot { background: var(--blue); }
.rp-report .rp-dot { background: var(--purple); }
.rp-critic .rp-dot { background: var(--pink); }

.rp-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; letter-spacing:.15em; text-transform:uppercase;
}
.rp-search .rp-label { color: var(--cyan); }
.rp-scrape .rp-label { color: var(--blue); }
.rp-report .rp-label { color: var(--purple); }
.rp-critic .rp-label { color: var(--pink); }

.rp-body {
    font-size: 0.9rem; line-height: 1.75; color: #b0bec5;
    white-space: pre-wrap; word-break: break-word;
    max-height: 380px; overflow-y: auto;
    scrollbar-width: thin; scrollbar-color: var(--border) transparent;
}

/* ══ SUCCESS ══════════════════════════════════════════════════════════════ */
.success-banner {
    background: linear-gradient(135deg,rgba(0,245,212,.1),rgba(123,47,255,.1));
    border: 1px solid rgba(0,245,212,.3);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    text-align: center;
    font-weight: 700;
    font-size: 1rem;
    color: var(--cyan);
    margin: 1.2rem 0 0.5rem;
}

/* ══ DOWNLOAD ═════════════════════════════════════════════════════════════ */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, var(--orange), var(--pink)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.65rem 2rem !important;
}

/* ══ IDLE ═════════════════════════════════════════════════════════════════ */
.idle-steps { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:2rem 0 1rem; }
.idle-box {
    border:1px solid var(--border); border-radius:14px;
    padding:1.1rem 0.8rem; text-align:center;
    background:var(--s1); opacity:.35;
}
.idle-icon { font-size:1.6rem; margin-bottom:5px; }
.idle-name { font-size:0.82rem; font-weight:600; }
.idle-sub  { font-size:0.68rem; color:var(--muted); margin-top:3px; }
.hint-text {
    text-align:center;
    font-family:'JetBrains Mono',monospace;
    font-size:0.72rem; color:var(--muted); letter-spacing:.08em; margin-top:0.5rem;
}

[data-testid="stSpinner"] > div { border-top-color: var(--cyan) !important; }
hr { border-color: var(--border) !important; }
.streamlit-expanderHeader {
    background: var(--s1) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--muted) !important;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-pill"><span></span> LangChain · Multi-Agent · AI Research</div>
  <div class="hero-title">
    <span class="w1">Autonomous</span> <span class="w2">Research</span><br>
    <span class="w3">Pipeline</span>
  </div>
  <p class="hero-sub">Four intelligent agents working in sequence — search, scrape, write, and critique — delivering a complete research report in minutes.</p>
</div>
""", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-shell"><div class="input-label">🔬 Research Topic</div>', unsafe_allow_html=True)
col_in, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_in:
    topic = st.text_input("topic", placeholder="e.g.  Breakthroughs in nuclear fusion energy 2025",
                          label_visibility="collapsed")
with col_btn:
    run = st.button("RUN →", use_container_width=True, disabled=not topic.strip())
st.markdown("</div>", unsafe_allow_html=True)

# ── STEP META ─────────────────────────────────────────────────────────────────
STEPS_META = [
    ("🔍", "Step 01", "Search Agent",  "Scours the web"),
    ("📄", "Step 02", "Reader Agent",  "Scrapes top URLs"),
    ("✍️", "Step 03", "Writer Chain",  "Drafts the report"),
    ("🎯", "Step 04", "Critic Chain",  "Reviews & scores"),
]

def render_steps(active: int = -1, done: list = []):
    boxes = ""
    for i, (icon, num, name, sub) in enumerate(STEPS_META):
        if i in done:
            cls = f"step-box done-{i}"
            tick = "✅"
        elif i == active:
            cls = f"step-box active active-{i}"
            tick = "⚡"
        else:
            cls = "step-box waiting"
            tick = ""
        boxes += f"""
        <div class="{cls}">
          <div class="step-num">{num}</div>
          <div class="step-icon">{icon}</div>
          <div class="step-name">{name}</div>
          <div class="step-sub">{sub}</div>
          <div class="step-tick">{tick}</div>
        </div>"""
    st.markdown(f'<div class="steps-row">{boxes}</div>', unsafe_allow_html=True)

def rp(cls: str, label: str, icon: str, content: str):
    safe = content.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""
    <div class="rp {cls}">
      <div class="rp-head"><div class="rp-dot"></div>
        <div class="rp-label">{icon} &nbsp; {label}</div>
      </div>
      <div class="rp-body">{safe}</div>
    </div>""", unsafe_allow_html=True)

# ── RUN ───────────────────────────────────────────────────────────────────────
if run and topic.strip():
    st.markdown("---")
    track = st.empty()
    results = {}

    try:
        with st.spinner("Loading agents…"):
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from multi_agent import build_reader_agent, build_search_agent, writer_chain, critic_chain

        # ── Step 1 ────────────────────────────────────────────────────────────
        with track.container():
            render_steps(active=0, done=[])

        with st.spinner("🔍  Search agent working…"):
            raw = build_search_agent().invoke({"messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]})
            last = raw["messages"][-1]
            results["search"] = extract_content(
                last.content if hasattr(last, "content") else last
            )

        with track.container():
            render_steps(active=1, done=[0])
        rp("rp-search", "Search Results", "🔍", results["search"])

        # ── Step 2 ────────────────────────────────────────────────────────────
        with st.spinner("📄  Reader agent scraping…"):
            raw2 = build_reader_agent().invoke({"messages": [
                ("user",
                 f"Based on the following search results about '{topic}', "
                 f"pick the most relevant URL and scrape it for deeper content.\n\n"
                 f"Search Results:\n{results['search'][:800]}")
            ]})
            last2 = raw2["messages"][-1]
            results["scraped"] = extract_content(
                last2.content if hasattr(last2, "content") else last2
            )

        with track.container():
            render_steps(active=2, done=[0, 1])
        rp("rp-scrape", "Scraped Content", "📄", results["scraped"])

        # ── Step 3 ────────────────────────────────────────────────────────────
        with st.spinner("✍️  Writer drafting report…"):
            combined = (f"SEARCH RESULTS:\n{results['search']}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{results['scraped']}")
            raw3 = writer_chain.invoke({"topic": topic, "research": combined})
            results["report"] = extract_content(raw3)

        with track.container():
            render_steps(active=3, done=[0, 1, 2])
        rp("rp-report", "Final Report", "✍️", results["report"])

        # ── Step 4 ────────────────────────────────────────────────────────────
        with st.spinner("🎯  Critic reviewing…"):
            raw4 = critic_chain.invoke({"report": results["report"]})
            results["feedback"] = extract_content(raw4)

        with track.container():
            render_steps(active=-1, done=[0, 1, 2, 3])
        rp("rp-critic", "Critic Feedback", "🎯", results["feedback"])

        st.markdown('<div class="success-banner">🎉 &nbsp; Pipeline completed successfully!</div>',
                    unsafe_allow_html=True)

        full_md = f"""# Research Report: {topic}

## Search Results
{results['search']}

## Scraped Content
{results['scraped']}

## Final Report
{results['report']}

## Critic Feedback
{results['feedback']}
"""
        st.download_button(
            "⬇  Download Full Report (.md)",
            data=full_md,
            file_name=f"research_{topic[:40].replace(' ','_')}.md",
            mime="text/markdown",
        )

    except ImportError as e:
        st.error(f"**Import Error** — make sure `multi_agent.py` is in the same folder.\n\n`{e}`")
    except Exception as e:
        st.error(f"**Pipeline Error:** {e}")
        raise

# ── IDLE ──────────────────────────────────────────────────────────────────────
else:
    idle = '<div class="idle-steps">'
    for icon, num, name, sub in STEPS_META:
        idle += f'<div class="idle-box"><div class="idle-icon">{icon}</div><div class="idle-name">{name}</div><div class="idle-sub">{sub}</div></div>'
    idle += '</div><p class="hint-text">↑ Enter a topic above and press RUN → to launch the pipeline</p>'
    st.markdown(idle, unsafe_allow_html=True)

    with st.expander("ℹ️  How it works"):
        st.markdown("""
**🔍 Search Agent** — Uses LangChain + web-search tools to find recent, reliable info about your topic.

**📄 Reader Agent** — Picks the most relevant URL from search results and scrapes it for deep content.

**✍️ Writer Chain** — Combines search + scraped data into a well-structured, comprehensive report.

**🎯 Critic Chain** — Reviews the report for accuracy, completeness, and quality with actionable feedback.
        """)