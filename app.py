"""
app.py — GTS Structured Trade Program Cockpit  (v2)

Reframed from a cross-sell scorer into a program-management cockpit that mirrors
the Sales Program Manager (GTS) role: managing live RF/SCF programs for GNB & IMM
clients, mobilising internal stakeholders, assuring revenue, surfacing expansion.

Tabs (deliberate order):
  1. Program Cockpit    — the day-job: live facilities, health, revenue assurance, cases
  2. Cross-Sell Pipeline — EV-ranked expansion with explainable score waterfalls
  3. Client Deep Dive   — single-client 360 + AI-generated call brief
  4. Portfolio Overview  — book-level analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import data
import engine
from ai_brief import build_brief_prompt, generate_brief

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GTS Program Cockpit",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ──────────────────────────────────────────────────────────────
RED   = "#DB0011"
AMBER = "#E8A317"
GREEN = "#3BAA6E"
DIM   = "#555555"
INK   = "#f0f0f0"
CARD  = "#161616"
BORDER = "#252525"

DARK_CHART = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font          = dict(color=INK, size=12),
    margin        = dict(l=4, r=4, t=28, b=4),
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{ font-family: 'IBM Plex Sans', system-ui, sans-serif; }}

.stApp {{
  background:
    radial-gradient(ellipse 1400px 500px at 85% -5%, #1c0406 0%, transparent 52%),
    #0e0e0e;
}}

/* ── Tabs ─────────────────────────────────────────── */
[data-baseweb="tab-list"] {{
  gap: 0.2rem; border-bottom: 1px solid {BORDER}; padding-bottom: 0;
}}
[data-baseweb="tab"] {{
  padding: 0.6rem 1.4rem; font-size: 0.82rem; font-weight: 500;
  letter-spacing: 0.3px; border-radius: 6px 6px 0 0; color: {DIM} !important;
  font-family: 'IBM Plex Mono', monospace;
}}
[aria-selected="true"] {{ color: {INK} !important; }}

/* ── Brand header ─────────────────────────────────── */
.brand {{ display:flex; align-items:flex-start; gap:14px; padding:4px 0 0 0; }}
.bmark {{
  width:22px; height:22px; background:{RED}; margin-top:4px; flex-shrink:0;
  clip-path: polygon(50% 0,100% 50%,50% 100%,0 50%,50% 0,18% 50%,50% 82%,82% 50%,50% 18%);
}}
.btitle {{
  font-size:1.45rem; font-weight:700; color:{INK}; letter-spacing:-0.3px; line-height:1.15;
}}
.bsub {{
  font-size:0.78rem; color:{DIM}; font-family:'IBM Plex Mono',monospace; margin-top:2px;
}}
.asof {{
  float:right; color:{DIM}; font-family:'IBM Plex Mono',monospace; font-size:0.74rem;
  margin-top:6px;
}}

/* ── KPI cards ────────────────────────────────────── */
.kpi {{
  background: linear-gradient(160deg, #181818, #121212);
  border: 1px solid {BORDER}; border-left: 3px solid {RED};
  border-radius: 10px; padding: 1rem 1.1rem;
}}
.kpi-lbl {{
  color: {DIM}; font-size: 0.67rem; text-transform: uppercase;
  letter-spacing: 1.3px; font-family: 'IBM Plex Mono', monospace;
}}
.kpi-val {{
  color: {INK}; font-size: 1.75rem; font-weight: 700; line-height: 1.1; margin-top: 4px;
}}
.kpi-sub {{ font-size: 0.76rem; margin-top: 2px; }}

/* ── Section eyebrow ──────────────────────────────── */
.eye {{
  font-family: 'IBM Plex Mono', monospace; color: {DIM}; font-size: 0.7rem;
  text-transform: uppercase; letter-spacing: 1.8px; margin: 0 0 8px 0;
}}

/* ── Panel header ─────────────────────────────────── */
.phdr {{
  font-size: 0.93rem; font-weight: 600; color: {INK};
  margin: 0 0 0.9rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid {BORDER};
}}

/* ── Verdict pills ────────────────────────────────── */
.pill {{
  display:inline-block; padding:2px 10px; border-radius:999px;
  font-family:'IBM Plex Mono',monospace; font-size:0.7rem; font-weight:500;
}}
.pill-red   {{ background:rgba(219,0,17,0.15); color:#ff6b78; border:1px solid rgba(219,0,17,0.35); }}
.pill-amber {{ background:rgba(232,163,23,0.13); color:{AMBER}; border:1px solid rgba(232,163,23,0.35); }}
.pill-green {{ background:rgba(59,170,110,0.13); color:{GREEN}; border:1px solid rgba(59,170,110,0.35); }}

/* ── Priority badges (pipeline) ───────────────────── */
.badge {{
  display:inline-block; padding:3px 11px; border-radius:999px;
  font-family:'IBM Plex Mono',monospace; font-size:0.68rem; font-weight:600;
}}
.b-high   {{ background:rgba(0,210,106,0.1); color:#00d26a; border:1px solid rgba(0,210,106,0.28); }}
.b-medium {{ background:rgba(232,163,23,0.1); color:{AMBER}; border:1px solid rgba(232,163,23,0.28); }}
.b-low    {{ background:rgba(120,120,120,0.1); color:#555; border:1px solid {BORDER}; }}

/* ── Flag line ────────────────────────────────────── */
.flag {{
  font-family: 'IBM Plex Mono', monospace; font-size: 0.79rem; color: #c0c0c0;
}}

/* ── Banker card ──────────────────────────────────── */
.bcard {{
  background: #1c1c1c; border: 1px solid {BORDER}; border-left: 3px solid {RED};
  border-radius: 7px; padding: 0.75rem 1rem; margin-bottom: 0.4rem;
}}
.bcard-role  {{
  font-size: 0.62rem; font-weight: 700; color: {RED};
  text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 4px;
  font-family: 'IBM Plex Mono', monospace;
}}
.bcard-name  {{ font-size: 0.88rem; font-weight: 600; color: {INK}; }}
.bcard-title {{ font-size: 0.72rem; color: {DIM}; margin-top: 2px; }}

/* ── Info strip ───────────────────────────────────── */
.istrip {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 9px;
  padding: 1rem 1.3rem; margin-bottom: 1.2rem;
}}
.irow {{ display:flex; flex-wrap:wrap; gap:1.75rem; margin-top:0.6rem; }}
.ii   {{ display:flex; flex-direction:column; }}
.ilbl {{ font-size:0.62rem; color:{DIM}; text-transform:uppercase; letter-spacing:1px;
         font-family:'IBM Plex Mono',monospace; }}
.ival {{ font-size:0.9rem; font-weight:600; color:{INK}; margin-top:1px; }}
.ctag {{
  display:inline-block; background:#1c1c1c; border:1px solid {BORDER};
  border-radius:4px; padding:2px 9px; font-size:0.72rem; color:#aaa;
  margin:2px; font-family:'IBM Plex Mono',monospace;
}}

/* ── Product pills ────────────────────────────────── */
.ppill {{
  display:inline-flex; align-items:center; gap:5px; padding:3px 9px;
  border-radius:5px; font-size:0.76rem; margin:2px; font-weight:500;
}}
.pp-on  {{ background:rgba(219,0,17,0.09); color:#ff4455; border:1px solid rgba(219,0,17,0.22); }}
.pp-off {{ background:#171717; color:#444; border:1px solid {BORDER}; }}

/* ── Sidebar ──────────────────────────────────────── */
[data-testid="stSidebar"] {{ background: #0d0d0d !important; border-right: 1px solid #1e1e1e; }}
.slbl {{
  font-size: 0.62rem; font-weight: 700; color: {RED};
  text-transform: uppercase; letter-spacing: 1.5px; margin: 1rem 0 0.25rem 0;
  font-family: 'IBM Plex Mono', monospace;
}}

/* ── Expander ─────────────────────────────────────── */
[data-testid="stExpander"] {{
  background: #141414 !important; border: 1px solid {BORDER} !important;
  border-radius: 8px !important; margin-bottom: 0.45rem;
}}

/* ── Misc ─────────────────────────────────────────── */
hr {{ border-color: #222 !important; margin: 1.5rem 0 !important; }}
.block-container {{ padding: 1.5rem 2.5rem 4rem; max-width: 1500px; }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def kpi_html(label, value, sub=None, sub_color=DIM):
    s = f"<div class='kpi-sub' style='color:{sub_color}'>{sub}</div>" if sub else ""
    return f"""<div class="kpi">
  <div class="kpi-lbl">{label}</div>
  <div class="kpi-val">{value}</div>{s}
</div>"""


def verdict_pill(v):
    cls = {"Action Required": "pill-red", "Watch": "pill-amber", "Healthy": "pill-green"}[v]
    return f"<span class='pill {cls}'>{v}</span>"


def priority_badge(label):
    cls = {"High": "b-high", "Medium": "b-medium", "Low": "b-low"}.get(label, "b-low")
    return f"<span class='badge {cls}'>{label}</span>"


def banker_card(role, name, title):
    return f"""<div class="bcard">
  <div class="bcard-role">{role}</div>
  <div class="bcard-name">{name}</div>
  <div class="bcard-title">{title}</div>
</div>"""


def dark(fig, **kw):
    fig.update_layout(**DARK_CHART, **kw)
    return fig


# ── Brand header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="brand">
  <div class="bmark"></div>
  <div>
    <span class="asof">DATA AS OF {data.AS_OF.strftime('%d %b %Y').upper()}</span>
    <div class="btitle">GTS Structured Trade Program Cockpit</div>
    <div class="bsub">Global Network Banking &amp; International Middle Market
      &nbsp;·&nbsp; Receivables &amp; Supply Chain Finance</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.write("")

# ── Session state ──────────────────────────────────────────────────────────────
if "focus_client" not in st.session_state:
    st.session_state.focus_client = None

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="slbl">Logged in as</p>', unsafe_allow_html=True)
    st.markdown("**J. Halász** · Sales Program Manager, GTS")
    st.caption("My book · GNB & IMM · New York")
    st.divider()

    st.markdown('<p class="slbl">Segment</p>', unsafe_allow_html=True)
    seg = st.multiselect("Segment", data.SEGMENTS, default=data.SEGMENTS, label_visibility="collapsed")

    st.markdown('<p class="slbl">Sector</p>', unsafe_allow_html=True)
    sectors_sel = st.multiselect("Sector", data.SECTORS, default=[], label_visibility="collapsed")

    st.markdown('<p class="slbl">Client Type</p>', unsafe_allow_html=True)
    ctype = st.multiselect(
        "Client type", ["US Domestic", "International Subsidiary"],
        default=["US Domestic", "International Subsidiary"], label_visibility="collapsed"
    )

    st.markdown('<p class="slbl">Min Cross-Sell Score</p>', unsafe_allow_html=True)
    min_score = st.slider("Score", 0, 100, 40, 5, label_visibility="collapsed")

    st.markdown('<p class="slbl">Business Line</p>', unsafe_allow_html=True)
    lines = st.multiselect("Line", data.BUSINESS_LINES, default=data.BUSINESS_LINES, label_visibility="collapsed")

    st.divider()
    st.caption("Mock data · Illustrative purposes only")


# ── Filter ─────────────────────────────────────────────────────────────────────
def _client_passes(c):
    if c["segment"] not in seg:                                  return False
    if sectors_sel and c["sector"] not in sectors_sel:           return False
    if c["client_type"] not in ctype:                            return False
    return True

clients_f    = [c for c in data.CLIENTS if _client_passes(c)]
client_ids_f = {c["id"] for c in clients_f}
programs_f   = [p for p in data.PROGRAMS if p["client_id"] in client_ids_f]

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Program Cockpit  ",
    "  Cross-Sell Pipeline  ",
    "  Client Deep Dive  ",
    "  Portfolio Overview  ",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PROGRAM COCKPIT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    summ = engine.portfolio_program_summary(programs_f)

    k1, k2, k3, k4, k5 = st.columns(5, gap="medium")
    k1.markdown(kpi_html("Live Programs",      summ["n_programs"]), unsafe_allow_html=True)
    k2.markdown(kpi_html("Total Limits",       f"${summ['total_limit_m']/1000:.1f}B",
                          f"{summ['avg_utilization']*100:.0f}% utilized"), unsafe_allow_html=True)
    k3.markdown(kpi_html("Expected Rev / mo",  f"${summ['expected_rev_k']/1000:.1f}M"), unsafe_allow_html=True)
    k4.markdown(kpi_html("Revenue Leakage",    f"${summ['rev_leakage_k']/1000:.2f}M",
                          "booked vs expected",
                          "#ff6b78" if summ["rev_leakage_k"] > 0 else GREEN), unsafe_allow_html=True)
    k5.markdown(kpi_html("Need Action",        str(summ["action_required"]),
                          f"+{summ['watch']} on watch", "#ff6b78"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2], gap="large")

    # Programs list — action first
    with col_l:
        st.markdown('<p class="eye">Programs by health · action-first</p>', unsafe_allow_html=True)
        rows = []
        for p in programs_f:
            h = engine.program_health(p)
            rows.append({**p, "verdict": h["verdict"], "flags": h["flags"]})
        order = {"Action Required": 0, "Watch": 1, "Healthy": 2}
        rows.sort(key=lambda r: (order[r["verdict"]], -r["drawn_usd_m"]))

        for r in rows[:14]:
            c1, c2 = st.columns([5, 1])
            flag_html = "".join(
                f" <span class='flag'>· {lbl}: {det}</span>"
                for lbl, det, _ in r["flags"][:3]
            )
            c1.markdown(
                f"<b>{r['client_name']}</b> &nbsp;"
                f"<span class='flag'>{r['type']} · {r['program_id']} · "
                f"${r['drawn_usd_m']:.0f}M / ${r['limit_usd_m']:.0f}M · "
                f"{r['days_to_rollover']}d to rollover</span><br>"
                + verdict_pill(r["verdict"]) + flag_html,
                unsafe_allow_html=True,
            )
            if c2.button("Open", key=f"open_{r['program_id']}"):
                st.session_state.focus_client = r["client_id"]
                st.info(f"Loaded {r['client_name']} — open the Client Deep Dive tab.")
            st.markdown("<hr style='margin:7px 0'>", unsafe_allow_html=True)

    # Revenue assurance + cases
    with col_r:
        st.markdown('<p class="phdr">Revenue Assurance · Booked vs Expected</p>', unsafe_allow_html=True)
        ra = pd.DataFrame([{
            "Client":   p["client_name"],
            "Expected": p["expected_rev_k_month"],
            "Booked":   p["booked_rev_k_month"],
            "Variance": p["rev_variance_k"],
        } for p in programs_f]).sort_values("Variance").head(10)

        fig_ra = go.Figure()
        fig_ra.add_bar(y=ra["Client"], x=ra["Expected"], orientation="h",
                       name="Expected", marker_color=DIM)
        fig_ra.add_bar(y=ra["Client"], x=ra["Booked"], orientation="h",
                       name="Booked", marker_color=RED)
        dark(fig_ra, barmode="overlay", height=320,
             legend=dict(orientation="h", y=1.1, font=dict(size=10, color=DIM),
                         bgcolor="rgba(0,0,0,0)"),
             xaxis=dict(title="$k / month", gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(tickfont=dict(size=9, color=DIM)))
        st.plotly_chart(fig_ra, use_container_width=True)

        st.markdown('<p class="phdr" style="margin-top:1rem">Open Cases · Stakeholder Mobilisation</p>',
                    unsafe_allow_html=True)
        open_cases = [
            c for c in data.CASES
            if c["status"] != "Resolved"
            and c["program_id"] in {p["program_id"] for p in programs_f}
        ]
        open_cases.sort(key=lambda c: (c["priority"] != "High", -c["age_days"]))
        for c in open_cases[:7]:
            breach = c["age_days"] > c["sla_days"]
            sla_html = (f"<span style='color:#ff6b78'>SLA +{c['age_days']-c['sla_days']}d</span>"
                        if breach else
                        f"<span style='color:{DIM}'>{c['age_days']}/{c['sla_days']}d</span>")
            st.markdown(
                f"<span class='flag'><b>{c['client_name']}</b> — {c['type']}<br>"
                f"→ {c['owner_team']} · {c['status']} · {c['priority']} · {sla_html}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("<hr style='margin:5px 0'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CROSS-SELL PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    opps = engine.get_all_opportunities(clients_f, min_score=min_score)
    opps = [o for o in opps if o["line"] in lines]

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    k1.markdown(kpi_html("Opportunities", len(opps)), unsafe_allow_html=True)
    k2.markdown(kpi_html("Total EV / mo",
                          f"${sum(o['expected_value_k'] for o in opps)/1000:.1f}M"),
                unsafe_allow_html=True)
    k3.markdown(kpi_html("High Priority",
                          str(sum(1 for o in opps if o["label"] == "High"))),
                unsafe_allow_html=True)
    avg_prop = sum(o["propensity"] for o in opps) / max(len(opps), 1) * 100
    k4.markdown(kpi_html("Avg Propensity", f"{avg_prop:.0f}%"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="eye">Ranked by expected value · propensity × revenue · top-of-book first</p>',
                unsafe_allow_html=True)

    df_pipe = pd.DataFrame([{
        "Client":        o["client_name"],
        "Product":       o["product"],
        "Line":          o["line"],
        "Score":         o["score"],
        "Priority":      o["label"],
        "Propensity %":  round(o["propensity"] * 100),
        "Rev $k/mo":     round(o["revenue_k_month"]),
        "EV $k/mo":      round(o["expected_value_k"]),
        "EV / effort":   o["ev_per_effort"],
    } for o in opps])

    def _color_priority(val):
        if val == "High":   return "background-color:rgba(0,210,106,0.09);color:#00d26a;font-weight:700"
        if val == "Medium": return "background-color:rgba(232,163,23,0.09);color:#E8A317;font-weight:700"
        return "color:#555"

    st.dataframe(
        df_pipe.style.map(_color_priority, subset=["Priority"]),
        use_container_width=True, height=320, hide_index=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="phdr">Top 5 — Explainable Score Waterfalls</p>', unsafe_allow_html=True)

    for o in opps[:5]:
        client_obj = data.get_client(o["client_id"])
        bankers    = data.get_bankers_for_opportunity(client_obj, o["product"])
        with st.expander(
            f"{o['client_name']}  —  {o['product']}   "
            f"[ {o['label']}  ·  score {o['score']}  ·  EV ${o['expected_value_k']:.0f}k/mo ]",
        ):
            wc1, wc2 = st.columns([3, 2])

            labels   = [c[0] for c in o["components"]] + ["Total"]
            vals     = [c[1] for c in o["components"]] + [0]
            measures = ["relative"] * len(o["components"]) + ["total"]
            wf = go.Figure(go.Waterfall(
                orientation="v", measure=measures, x=labels, y=vals,
                connector={"line": {"color": BORDER}},
                increasing={"marker": {"color": RED}},
                totals={"marker": {"color": INK}},
            ))
            dark(wf, height=260, yaxis_title="score pts",
                 xaxis=dict(tickfont=dict(size=10, color=DIM), gridcolor=BORDER),
                 yaxis=dict(gridcolor=BORDER, tickfont=dict(color=DIM)))
            wc1.plotly_chart(wf, use_container_width=True)

            rm_n, rm_t = bankers["rm"]
            specs_str  = ", ".join(s[0] for s in bankers["specialists"])
            wc2.markdown(
                f"**Propensity (lookalike):** {o['propensity']*100:.0f}%  \n"
                f"**Est. revenue:** ${o['revenue_k_month']:.0f}k/mo @ {o['margin_bps']}bps  \n"
                f"**Expected value:** ${o['expected_value_k']:.0f}k/mo  \n"
                f"**Effort:** ~{o['effort_days']} RM-days · EV/effort {o['ev_per_effort']}  \n\n"
                f"**RM:** {rm_n} ({rm_t})  \n"
                f"**Specialist:** {specs_str}  \n\n"
                f"_{engine.recommended_action(o['label'])}_"
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CLIENT DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="eye">Client Deep Dive</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    names       = {c["name"]: c["id"] for c in data.CLIENTS}
    default_idx = 0
    if st.session_state.focus_client:
        fc = data.get_client(st.session_state.focus_client)
        if fc and fc["name"] in names:
            default_idx = list(names.keys()).index(fc["name"])
    sel_name = st.selectbox("Client", list(names.keys()), index=default_idx,
                             label_visibility="collapsed")
    c        = data.get_client(names[sel_name])
    st.markdown("<br>", unsafe_allow_html=True)

    # Info strip
    corridors_html = "".join(f'<span class="ctag">{g}</span>' for g in c["trade_corridors"])
    st.markdown(f"""
<div class="istrip">
  <div style="font-size:1.1rem;font-weight:700;color:{INK};margin-bottom:0.65rem">
    {c['name']}
    <span style="font-size:0.75rem;font-weight:400;color:{DIM};margin-left:12px">{c['client_type']}</span>
  </div>
  <div class="irow">
    <div class="ii"><span class="ilbl">Sector</span><span class="ival">{c['sector']}</span></div>
    <div class="ii"><span class="ilbl">Segment</span><span class="ival">{c['segment']}</span></div>
    <div class="ii"><span class="ilbl">HQ</span><span class="ival">{c['hq']}</span></div>
    <div class="ii"><span class="ilbl">Revenue</span><span class="ival">${c['revenue_usd_m']/1000:.1f}B</span></div>
    <div class="ii"><span class="ilbl">Trade Volume</span><span class="ival">${c['trade_volume_usd_m']/1000:.1f}B</span></div>
    <div class="ii"><span class="ilbl">DSO</span><span class="ival">{c['dso']}d</span></div>
    <div class="ii"><span class="ilbl">DPO</span><span class="ival">{c['dpo']}d</span></div>
    <div class="ii"><span class="ilbl">Suppliers</span><span class="ival">{c['supplier_count']:,}</span></div>
    <div class="ii"><span class="ilbl">Relationship</span><span class="ival">{c['relationship_years']} yrs</span></div>
  </div>
  <div style="margin-top:0.75rem">{corridors_html}</div>
</div>
""", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2], gap="large")

    # Live programs + gauge
    with col_a:
        st.markdown('<p class="phdr">Live Structured Programs</p>', unsafe_allow_html=True)
        cps = data.get_programs_for_client(c["id"])
        if not cps:
            st.caption("No structured RF/SCF programs on this client yet — see cross-sell below.")
        for p in cps:
            h    = engine.program_health(p)
            util = p["utilization"]
            gauge_color = RED if util > 1 else (AMBER if util >= 0.9 else GREEN)
            g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=util * 100,
                number={"suffix": "%", "font": {"color": INK, "size": 20}},
                gauge={
                    "axis": {"range": [0, 120], "tickcolor": DIM, "tickfont": {"color": DIM}},
                    "bar":  {"color": gauge_color},
                    "steps": [
                        {"range": [0, 90],   "color": "#1c1c1c"},
                        {"range": [90, 100], "color": "#332700"},
                        {"range": [100, 120],"color": "#330306"},
                    ],
                    "threshold": {"line": {"color": RED, "width": 2}, "value": 100},
                },
                title={"text": f"{p['type']} {p['program_id']} · ${p['drawn_usd_m']:.0f}M / ${p['limit_usd_m']:.0f}M",
                       "font": {"size": 11, "color": DIM}},
            ))
            g.update_layout(height=190, margin=dict(l=12, r=12, t=36, b=0),
                            paper_bgcolor="rgba(0,0,0,0)", font_color=INK)
            st.plotly_chart(g, use_container_width=True)

            flag_html = " ".join(
                f"<span class='flag'>· {lbl}: {det}</span>"
                for lbl, det, _ in h["flags"]
            )
            st.markdown(verdict_pill(h["verdict"]) + " " + flag_html, unsafe_allow_html=True)

            # Supplier funnel for SCF
            if p["type"] == "SCF":
                sup = data.get_suppliers_for_program(p["program_id"])
                if sup:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<p class="eye">Supplier onboarding funnel</p>', unsafe_allow_html=True)
                    funnel = go.Figure(go.Funnel(
                        y=["Invited", "KYC in progress", "Onboarded", "Actively discounting"],
                        x=[sup["invited"], sup["kyc_in_progress"],
                           sup["onboarded"], sup["actively_discounting"]],
                        marker={"color": [BORDER, DIM, AMBER, GREEN]},
                        textposition="inside",
                        textinfo="value+percent initial",
                    ))
                    dark(funnel, height=200, margin=dict(l=0, r=0, t=4, b=0),
                         font=dict(color=INK, size=11))
                    st.plotly_chart(funnel, use_container_width=True)

            st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

    # Cross-sell EV chart + AI brief
    with col_b:
        st.markdown('<p class="phdr">Cross-Sell EV by Product</p>', unsafe_allow_html=True)
        client_opps = engine.analyze_client(c)[:10]
        bar_df = pd.DataFrame([{
            "Product":  o["product"], "EV": o["expected_value_k"], "Priority": o["label"]
        } for o in client_opps])
        fig_bar = px.bar(
            bar_df, x="EV", y="Product", orientation="h", color="Priority",
            color_discrete_map={"High": RED, "Medium": AMBER, "Low": "#2a2a2a"},
        )
        dark(fig_bar, height=340,
             xaxis=dict(title="EV $k/mo", gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(tickfont=dict(size=9, color=DIM), autorange="reversed",
                        gridcolor="rgba(0,0,0,0)"),
             showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown('<p class="phdr" style="margin-top:1rem">AI Call Brief</p>',
                    unsafe_allow_html=True)
        st.caption("Generate RM-ready talking points from this client's profile.")
        if st.button("Generate call brief", key="aibrief"):
            with st.spinner("Drafting brief..."):
                st.session_state["brief_text"]   = generate_brief(c, client_opps)
                st.session_state["brief_prompt"] = build_brief_prompt(c, client_opps)
        if st.session_state.get("brief_text"):
            st.markdown(st.session_state["brief_text"])
            with st.expander("View prompt sent to model"):
                st.code(st.session_state["brief_prompt"], language="text")

    # Call brief detail (full-width)
    st.divider()
    st.markdown('<p class="phdr">Call Brief — Top Opportunities</p>', unsafe_allow_html=True)
    st.caption("Expand any row to see the rationale and bankers to loop in")

    call_opps = sorted(
        [o for o in engine.analyze_client(c) if o["score"] >= min_score],
        key=lambda x: x["expected_value_k"], reverse=True,
    )
    if not call_opps:
        st.info("No opportunities above the score threshold for this client.")
    else:
        for opp in call_opps[:8]:
            lbl = opp["label"]
            with st.expander(
                f"{opp['product']}   ·   {opp['score']}/100   ·   EV ${opp['expected_value_k']:.0f}k/mo   ·   {lbl}",
                expanded=opp["score"] >= 70,
            ):
                bankers = data.get_bankers_for_opportunity(c, opp["product"])
                b1, b2  = st.columns(2)
                rm_n, rm_t = bankers["rm"]
                b1.markdown(banker_card("Relationship Manager", rm_n, rm_t), unsafe_allow_html=True)
                for sn, st_ in bankers["specialists"][:2]:
                    b2.markdown(banker_card("Product Specialist", sn, st_), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(priority_badge(lbl), unsafe_allow_html=True)
                st.markdown("&nbsp; **Why this opportunity**", unsafe_allow_html=True)
                for lbl2, pts in opp["components"]:
                    if lbl2 != "Base":
                        st.markdown(f"- {lbl2} (+{pts} pts)")

                if opp["score"] >= 70:
                    st.success(f"Recommended action: {engine.recommended_action('High')}")
                elif opp["score"] >= 40:
                    st.warning(f"Recommended action: {engine.recommended_action('Medium')}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PORTFOLIO OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    tv      = sum(c["trade_volume_usd_m"] for c in clients_f)
    all_opp = engine.get_all_opportunities(clients_f, min_score=0)
    avg_enr = sum(len(c["enrolled"]) for c in clients_f) / max(len(clients_f), 1)

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    k1.markdown(kpi_html("Clients in View",       str(len(clients_f))),     unsafe_allow_html=True)
    k2.markdown(kpi_html("Total Trade Volume",    f"${tv/1000:.1f}B"),       unsafe_allow_html=True)
    k3.markdown(kpi_html("Cross-Sell EV / mo",
                          f"${sum(o['expected_value_k'] for o in all_opp)/1000:.1f}M"),
                unsafe_allow_html=True)
    k4.markdown(kpi_html("Avg Products / Client", f"{avg_enr:.1f}",
                          f"of {len(data.PRODUCTS)}"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    o1, o2 = st.columns(2, gap="large")

    with o1:
        st.markdown('<p class="phdr">Working Capital Map · DSO vs DPO</p>', unsafe_allow_html=True)
        wc_df = pd.DataFrame([{
            "DSO": c["dso"], "DPO": c["dpo"],
            "Trade Vol": c["trade_volume_usd_m"],
            "Sector": c["sector"], "Client": c["name"],
        } for c in clients_f])
        fig_wc = px.scatter(
            wc_df, x="DSO", y="DPO", size="Trade Vol",
            color="Sector", hover_name="Client", size_max=28,
        )
        dark(fig_wc, height=420,
             xaxis=dict(gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(gridcolor=BORDER, tickfont=dict(color=DIM)),
             legend=dict(font=dict(size=10, color=DIM), bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_wc, use_container_width=True)

    with o2:
        st.markdown('<p class="phdr">Avg Cross-Sell EV by Product</p>', unsafe_allow_html=True)
        from collections import defaultdict
        agg = defaultdict(list)
        for o in all_opp:
            agg[o["product"]].append(o["expected_value_k"])
        ev_df = pd.DataFrame([{
            "Product": k, "Avg EV": round(sum(v) / len(v), 1)
        } for k, v in agg.items()]).sort_values("Avg EV")
        fig_ev = px.bar(ev_df, x="Avg EV", y="Product", orientation="h")
        fig_ev.update_traces(marker_color=RED)
        dark(fig_ev, height=420,
             xaxis=dict(title="EV $k/mo", gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(tickfont=dict(size=9, color=DIM), gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_ev, use_container_width=True)
