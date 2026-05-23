"""GTS Cross-Sell Intelligence Engine — Portfolio demo for HSBC Sales Program Manager role."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import CLIENTS, GTS_PRODUCTS, PRODUCT_CATEGORIES, get_portfolio_df, get_bankers_for_opportunity
from engine import analyze_client, get_all_opportunities, score_label, product_category

st.set_page_config(
    page_title="GTS Cross-Sell Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ──────────────────────────────────────────────────────────────
RED      = "#DB0011"
BG_CARD  = "#161616"
BG_CARD2 = "#1c1c1c"
BORDER   = "#2a2a2a"
TXT      = "#f0f0f0"
DIM      = "#777777"
GREEN    = "#00d26a"
AMBER    = "#f59e0b"

DARK_CHART = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font          = dict(color=TXT, size=12),
    margin        = dict(l=4, r=4, t=28, b=4),
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Layout ─────────────────────────────────────────── */
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1440px; }

/* ── Tabs ───────────────────────────────────────────── */
[data-baseweb="tab-list"] {
  gap: 0.25rem;
  border-bottom: 1px solid #252525;
  padding-bottom: 0;
}
[data-baseweb="tab"] {
  padding: 0.55rem 1.4rem;
  font-size: 0.83rem;
  font-weight: 500;
  letter-spacing: 0.4px;
  border-radius: 6px 6px 0 0;
  color: #777 !important;
}
[aria-selected="true"] { color: #f0f0f0 !important; }

/* ── KPI cards ──────────────────────────────────────── */
.kpi {
  background: #161616;
  border: 1px solid #252525;
  border-top: 3px solid #DB0011;
  border-radius: 8px;
  padding: 1.2rem 1.4rem 1.1rem;
}
.kpi-lbl {
  font-size: 0.65rem; font-weight: 700; color: #666;
  text-transform: uppercase; letter-spacing: 1.4px;
  margin-bottom: 0.4rem;
}
.kpi-val {
  font-size: 1.75rem; font-weight: 700; color: #f0f0f0; line-height: 1.1;
}
.kpi-sub { font-size: 0.72rem; color: #555; margin-top: 0.25rem; }

/* ── Section / panel labels ─────────────────────────── */
.eyebrow {
  font-size: 0.63rem; font-weight: 700; color: #DB0011;
  text-transform: uppercase; letter-spacing: 2px;
  margin: 0 0 0.5rem 0;
}
.panel-hdr {
  font-size: 0.95rem; font-weight: 600; color: #f0f0f0;
  margin: 0 0 1.1rem 0; padding-bottom: 0.55rem;
  border-bottom: 1px solid #252525;
}

/* ── Priority badges ────────────────────────────────── */
.badge {
  display: inline-block; padding: 3px 11px; border-radius: 20px;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.6px;
}
.b-high   { background: rgba(0,210,106,0.11); color: #00d26a; border: 1px solid rgba(0,210,106,0.28); }
.b-medium { background: rgba(245,158,11,0.11); color: #f59e0b; border: 1px solid rgba(245,158,11,0.28); }
.b-low    { background: rgba(120,120,120,0.1); color: #666; border: 1px solid #2a2a2a; }

/* ── Product pills ──────────────────────────────────── */
.ppill {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 10px; border-radius: 5px; font-size: 0.77rem;
  margin: 2px 2px; font-weight: 500; white-space: nowrap;
}
.pp-on  { background: rgba(219,0,17,0.09); color: #ff4455; border: 1px solid rgba(219,0,17,0.22); }
.pp-off { background: #171717; color: #444; border: 1px solid #252525; }

/* ── Banker cards ───────────────────────────────────── */
.bcard {
  background: #1c1c1c;
  border: 1px solid #252525;
  border-left: 3px solid #DB0011;
  border-radius: 7px;
  padding: 0.8rem 1rem;
  margin-bottom: 0.45rem;
}
.bcard-role  { font-size: 0.62rem; font-weight: 700; color: #DB0011;
               text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 5px; }
.bcard-name  { font-size: 0.9rem; font-weight: 600; color: #f0f0f0; }
.bcard-title { font-size: 0.73rem; color: #777; margin-top: 2px; }

/* ── Info strip ─────────────────────────────────────── */
.istrip {
  background: #161616;
  border: 1px solid #252525;
  border-radius: 9px;
  padding: 1.1rem 1.4rem;
  margin-bottom: 1.25rem;
}
.irow { display: flex; flex-wrap: wrap; gap: 2rem; margin-top: 0.6rem; }
.iitem { display: flex; flex-direction: column; }
.ilbl  { font-size: 0.62rem; color: #555; text-transform: uppercase; letter-spacing: 1.1px; }
.ival  { font-size: 0.9rem; font-weight: 600; color: #f0f0f0; margin-top: 1px; }
.ctag  {
  display: inline-block; background: #1c1c1c; border: 1px solid #252525;
  border-radius: 4px; padding: 2px 9px; font-size: 0.73rem; color: #aaa;
  margin: 2px; font-family: monospace; letter-spacing: 0.5px;
}

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] { background: #0a0a0a !important; border-right: 1px solid #1e1e1e; }
.slbl {
  font-size: 0.62rem; font-weight: 700; color: #DB0011;
  text-transform: uppercase; letter-spacing: 1.5px;
  margin: 1.1rem 0 0.3rem 0;
}

/* ── Expanders ──────────────────────────────────────── */
[data-testid="stExpander"] {
  background: #141414 !important;
  border: 1px solid #252525 !important;
  border-radius: 8px !important;
  margin-bottom: 0.45rem;
}

/* ── Divider ────────────────────────────────────────── */
hr { border-color: #222 !important; margin: 1.75rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def kpi(label, value, sub=""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""<div class="kpi">
  <div class="kpi-lbl">{label}</div>
  <div class="kpi-val">{value}</div>
  {sub_html}
</div>"""


def badge(label):
    cls = {"High": "b-high", "Medium": "b-medium", "Low": "b-low"}.get(label, "b-low")
    return f'<span class="badge {cls}">{label}</span>'


def dark(fig, **extra):
    fig.update_layout(**DARK_CHART, **extra)
    return fig


def banker_card(role, name, title):
    return f"""<div class="bcard">
  <div class="bcard-role">{role}</div>
  <div class="bcard-name">{name}</div>
  <div class="bcard-title">{title}</div>
</div>"""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/HSBC_logo_%282018%29.svg/320px-HSBC_logo_%282018%29.svg.png",
        width=130,
    )
    st.markdown("### Cross-Sell Engine")
    st.caption("US & International Subsidiary Portfolio")
    st.divider()

    st.markdown('<p class="slbl">Client Type</p>', unsafe_allow_html=True)
    client_types = ["US Domestic", "International Subsidiary"]
    selected_types = st.multiselect("Client Type", client_types, default=client_types, label_visibility="collapsed")

    st.markdown('<p class="slbl">Sector</p>', unsafe_allow_html=True)
    sectors = sorted({c["sector"] for c in CLIENTS})
    selected_sectors = st.multiselect("Sector", sectors, default=sectors, label_visibility="collapsed")

    st.markdown('<p class="slbl">Min Opportunity Score</p>', unsafe_allow_html=True)
    min_score = st.slider("Score", 0, 100, 40, label_visibility="collapsed")

    st.markdown('<p class="slbl">Business Line</p>', unsafe_allow_html=True)
    selected_categories = st.multiselect(
        "Business Line", list(PRODUCT_CATEGORIES.keys()),
        default=list(PRODUCT_CATEGORIES.keys()), label_visibility="collapsed"
    )
    products_filter = [p for cat in selected_categories for p in PRODUCT_CATEGORIES.get(cat, [])]

    st.divider()
    st.caption("Mock data · Illustrative purposes only")


# ── Filter ─────────────────────────────────────────────────────────────────────
filtered_clients = [
    c for c in CLIENTS
    if c["sector"] in selected_sectors and c["client_type"] in selected_types
]
all_opps     = get_all_opportunities(filtered_clients)
filtered_opps = [o for o in all_opps if o["score"] >= min_score and o["product"] in products_filter]

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_dash, tab_pipe, tab_client = st.tabs([
    "   Portfolio Overview   ",
    "   Opportunity Pipeline   ",
    "   Client Deep Dive   ",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Portfolio Overview
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    st.markdown('<p class="eyebrow">US & International Subsidiary · Trade Finance Portfolio</p>', unsafe_allow_html=True)
    st.caption(f"{len(filtered_clients)} clients · {len(filtered_opps)} cross-sell opportunities identified")
    st.markdown("<br>", unsafe_allow_html=True)

    total_vol   = sum(c["trade_volume_usd_m"] for c in filtered_clients)
    rev_upside  = sum(o["estimated_revenue_usd_k"] for o in filtered_opps) / 1000
    high_ct     = sum(1 for o in filtered_opps if o["score"] >= 70)
    avg_prods   = sum(len(c["current_products"]) for c in filtered_clients) / max(len(filtered_clients), 1)

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    k1.markdown(kpi("Total Trade Volume",          f"${total_vol:,.0f}M",  f"{len(filtered_clients)} clients"), unsafe_allow_html=True)
    k2.markdown(kpi("Cross-Sell Revenue Upside",   f"${rev_upside:,.1f}M", "indicative annual"), unsafe_allow_html=True)
    k3.markdown(kpi("High-Priority Opportunities", str(high_ct),            "score ≥ 70"), unsafe_allow_html=True)
    k4.markdown(kpi("Avg Products / Client",       f"{avg_prods:.1f}",      f"of {len(GTS_PRODUCTS)} products"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown('<p class="panel-hdr">Product Penetration by Client</p>', unsafe_allow_html=True)
        matrix_rows = []
        for c in filtered_clients:
            row = {"Client": c["client"]}
            for p in GTS_PRODUCTS:
                row[p] = 1 if p in c["current_products"] else 0
            matrix_rows.append(row)
        df_mat = pd.DataFrame(matrix_rows).set_index("Client")

        fig_heat = px.imshow(
            df_mat,
            color_continuous_scale=[[0, "#1a1a1a"], [1, RED]],
            aspect="auto",
            labels={"color": "Enrolled"},
        )
        fig_heat.update_traces(showscale=False)
        dark(fig_heat, height=430,
             xaxis=dict(tickangle=-35, tickfont=dict(size=9, color=DIM), gridcolor=BORDER),
             yaxis=dict(tickfont=dict(size=9, color=DIM), gridcolor=BORDER))
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_r:
        st.markdown('<p class="panel-hdr">Avg Opportunity Score by Product</p>', unsafe_allow_html=True)
        prod_scores = {}
        for p in GTS_PRODUCTS:
            s = [o["score"] for o in filtered_opps if o["product"] == p]
            prod_scores[p] = sum(s) / len(s) if s else 0

        df_ps = pd.DataFrame([{"Product": k, "Score": v} for k, v in prod_scores.items()]).sort_values("Score")
        fig_ps = px.bar(
            df_ps, x="Score", y="Product", orientation="h",
            color="Score",
            color_continuous_scale=[[0, "#2a0005"], [0.5, "#7a0008"], [1, RED]],
        )
        dark(fig_ps, height=340, showlegend=False, coloraxis_showscale=False,
             xaxis=dict(range=[0, 100], gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(tickfont=dict(size=9, color=DIM), gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_ps, use_container_width=True)

        st.markdown('<p class="panel-hdr" style="margin-top:1.25rem">Working Capital Positioning</p>', unsafe_allow_html=True)
        df_sc = get_portfolio_df()
        df_sc = df_sc[df_sc["Sector"].isin(selected_sectors)]
        fig_sc = px.scatter(
            df_sc, x="DSO (days)", y="DPO (days)",
            size="Trade Volume ($M)", color="Sector",
            hover_name="Client", size_max=28,
        )
        dark(fig_sc, height=270,
             xaxis=dict(gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(gridcolor=BORDER, tickfont=dict(color=DIM)),
             legend=dict(font=dict(size=10, color=DIM), bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_sc, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Opportunity Pipeline
# ══════════════════════════════════════════════════════════════════════════════
with tab_pipe:
    st.markdown('<p class="eyebrow">Cross-Sell Opportunity Pipeline · Ranked by Score</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered_opps:
        st.info("No opportunities match current filters. Adjust the sidebar filters.")
    else:
        df_opps = pd.DataFrame([{
            "Client":             o["client"],
            "Type":               o.get("client_type", ""),
            "Sector":             o["sector"],
            "Product":            o["product"],
            "Score":              o["score"],
            "Priority":           score_label(o["score"]),
            "Est. Revenue ($K)":  o["estimated_revenue_usd_k"],
            "Relationship (yrs)": o["relationship_years"],
        } for o in filtered_opps]).sort_values("Score", ascending=False)

        def color_priority(val):
            if val == "High":
                return "background-color: rgba(0,210,106,0.10); color: #00d26a; font-weight: 700"
            if val == "Medium":
                return "background-color: rgba(245,158,11,0.10); color: #f59e0b; font-weight: 700"
            return "color: #555"

        styled = df_opps.style.map(color_priority, subset=["Priority"])
        st.dataframe(styled, use_container_width=True, hide_index=True, height=420)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="panel-hdr">Top Priority Actions</p>', unsafe_allow_html=True)

        top5 = [o for o in filtered_opps if o["score"] >= 70][:5] or filtered_opps[:3]

        for opp in top5:
            cd = next((c for c in CLIENTS if c["client"] == opp["client"]), None)
            lbl = score_label(opp["score"])
            with st.expander(
                f"{opp['client']}   ·   {opp['product']}   ·   {opp['score']}/100   ·   ${opp['estimated_revenue_usd_k']:,}K",
                expanded=False,
            ):
                st.markdown(badge(lbl) + "&nbsp;&nbsp;", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                m1.metric("Opportunity Score",   f"{opp['score']} / 100")
                m2.metric("Est. Annual Revenue", f"${opp['estimated_revenue_usd_k']:,}K")
                m3.metric("Relationship",        f"{opp['relationship_years']} yrs")
                st.markdown("<br>", unsafe_allow_html=True)

                if cd:
                    bankers = get_bankers_for_opportunity(cd, opp["product"])
                    b1, b2 = st.columns(2)
                    rm_n, rm_t = bankers["rm"]
                    b1.markdown(banker_card("Relationship Manager", rm_n, rm_t), unsafe_allow_html=True)
                    if bankers["specialists"]:
                        sn, st_ = bankers["specialists"][0]
                        b2.markdown(banker_card("Product Specialist", sn, st_), unsafe_allow_html=True)

                st.markdown("**Why this opportunity**")
                for pt in opp["rationale"]:
                    st.markdown(f"- {pt}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Client Deep Dive
# ══════════════════════════════════════════════════════════════════════════════
with tab_client:
    st.markdown('<p class="eyebrow">Client Deep Dive</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    client_names  = [c["client"] for c in filtered_clients]
    selected_name = st.selectbox("Select client", client_names, label_visibility="collapsed")
    client_data   = next(c for c in CLIENTS if c["client"] == selected_name)
    scored        = analyze_client(client_data)

    st.markdown("<br>", unsafe_allow_html=True)

    # Info strip
    corridors_html = "".join(f'<span class="ctag">{g}</span>' for g in client_data["trade_geographies"])
    st.markdown(f"""
<div class="istrip">
  <div style="font-size:1.1rem;font-weight:700;color:#f0f0f0;margin-bottom:0.7rem">
    {client_data['client']}
    <span style="font-size:0.75rem;font-weight:400;color:#555;margin-left:12px">{client_data['client_type']}</span>
  </div>
  <div class="irow">
    <div class="iitem"><span class="ilbl">Sector</span><span class="ival">{client_data['sector']}</span></div>
    <div class="iitem"><span class="ilbl">HQ</span><span class="ival">{client_data['hq']}</span></div>
    <div class="iitem"><span class="ilbl">Relationship</span><span class="ival">{client_data['relationship_years']} yrs</span></div>
    <div class="iitem"><span class="ilbl">Revenue</span><span class="ival">${client_data['annual_revenue_usd_m']}M</span></div>
    <div class="iitem"><span class="ilbl">Trade Volume</span><span class="ival">${client_data['trade_volume_usd_m']}M</span></div>
    <div class="iitem"><span class="ilbl">DSO</span><span class="ival">{client_data['dso_days']}d</span></div>
    <div class="iitem"><span class="ilbl">DPO</span><span class="ival">{client_data['dpo_days']}d</span></div>
    <div class="iitem"><span class="ilbl">Suppliers</span><span class="ival">{client_data['supplier_count']:,}</span></div>
    <div class="iitem"><span class="ilbl">Geographies</span><span class="ival">{len(client_data['trade_geographies'])}</span></div>
  </div>
  <div style="margin-top:0.8rem">{corridors_html}</div>
</div>
""", unsafe_allow_html=True)

    col_cov, col_chart = st.columns([2, 3], gap="large")

    with col_cov:
        st.markdown('<p class="panel-hdr">Product Coverage</p>', unsafe_allow_html=True)
        existing = client_data["current_products"]
        for cat, prods in PRODUCT_CATEGORIES.items():
            st.markdown(f'<p class="eyebrow" style="margin-top:0.9rem">{cat}</p>', unsafe_allow_html=True)
            pills = ""
            for p in prods:
                short = p.split(" - ", 1)[-1] if " - " in p else p
                cls   = "pp-on" if p in existing else "pp-off"
                dot   = "●" if p in existing else "○"
                pills += f'<span class="ppill {cls}">{dot}&nbsp;{short}</span>'
            st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:2px;margin-bottom:0.3rem">{pills}</div>', unsafe_allow_html=True)

    with col_chart:
        st.markdown('<p class="panel-hdr">Cross-Sell Opportunity Scores</p>', unsafe_allow_html=True)
        df_sc2 = pd.DataFrame([{
            "Product":  s["product"],
            "Score":    s["score"],
            "Category": product_category(s["product"]),
            "Status":   "Enrolled" if s["already_enrolled"] else score_label(s["score"]),
        } for s in scored]).sort_values("Score")

        cmap = {"Enrolled": "#2a2a2a", "High": RED, "Medium": AMBER, "Low": "#303030"}
        fig_opp = px.bar(
            df_sc2, x="Score", y="Product", orientation="h",
            color="Status", color_discrete_map=cmap,
            category_orders={"Status": ["Enrolled", "Low", "Medium", "High"]},
        )
        dark(fig_opp, height=500,
             xaxis=dict(range=[0, 100], title="Score", gridcolor=BORDER, tickfont=dict(color=DIM)),
             yaxis=dict(tickfont=dict(size=9, color=DIM), gridcolor="rgba(0,0,0,0)"),
             legend=dict(title="Priority", font=dict(size=10, color=DIM), bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_opp, use_container_width=True)

    st.divider()

    # Call Brief
    st.markdown('<p class="panel-hdr">Call Brief — Top Opportunities</p>', unsafe_allow_html=True)
    st.caption("Expand any row to see rationale and the bankers to loop in")

    new_opps = sorted(
        [s for s in scored if not s["already_enrolled"] and s["score"] >= 40],
        key=lambda x: x["score"], reverse=True
    )

    if not new_opps:
        st.info("This client is fully enrolled or no high-confidence opportunities exist above the threshold.")
    else:
        for opp in new_opps[:8]:
            lbl = score_label(opp["score"])
            with st.expander(
                f"{opp['product']}   ·   {opp['score']}/100   ·   ${opp['estimated_revenue_usd_k']:,}K   ·   {lbl}",
                expanded=opp["score"] >= 70,
            ):
                bankers = get_bankers_for_opportunity(client_data, opp["product"])
                b_col, r_col = st.columns(2)

                rm_n, rm_t = bankers["rm"]
                b_col.markdown(banker_card("Relationship Manager", rm_n, rm_t), unsafe_allow_html=True)

                for sn, st_ in bankers["specialists"][:2]:
                    r_col.markdown(banker_card("Product Specialist", sn, st_), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Why this opportunity**")
                for pt in opp["rationale"]:
                    st.markdown(f"- {pt}")

                if opp["score"] >= 70:
                    st.success("Recommended action: Schedule intro with product specialist this quarter")
                elif opp["score"] >= 40:
                    st.warning("Recommended action: Qualify further in next relationship review")
