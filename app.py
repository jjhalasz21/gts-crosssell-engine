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

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; }
  .metric-card {
    background: #f8f9fa; border-radius: 8px; padding: 1rem 1.25rem;
    border-left: 4px solid #DB0011; margin-bottom: 0.75rem;
  }
  .score-high { color: #1a7a1a; font-weight: 700; }
  .score-medium { color: #c47a00; font-weight: 700; }
  .score-low { color: #888; font-weight: 600; }
  .pill {
    display: inline-block; padding: 2px 10px; border-radius: 12px;
    font-size: 0.78rem; font-weight: 600; margin: 2px;
  }
  .pill-existing { background: #e8f4e8; color: #1a7a1a; }
  .pill-new { background: #fff3cd; color: #856404; }
  .rationale-item { margin: 4px 0; font-size: 0.9rem; color: #444; }
  .sidebar-header { font-size: 0.8rem; color: #999; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/HSBC_logo_%282018%29.svg/320px-HSBC_logo_%282018%29.svg.png",
        width=140,
    )
    st.markdown("## Cross-Sell Engine")
    st.caption("US & International Subsidiary Portfolio")
    st.divider()

    st.markdown('<p class="sidebar-header">Filters</p>', unsafe_allow_html=True)

    client_types = ["US Domestic", "International Subsidiary"]
    selected_types = st.multiselect("Client Type", client_types, default=client_types)

    sectors = sorted({c["sector"] for c in CLIENTS})
    selected_sectors = st.multiselect("Sector", sectors, default=sectors)

    min_score = st.slider("Min Opportunity Score", 0, 100, 40)

    st.markdown('<p class="sidebar-header">Product Lines</p>', unsafe_allow_html=True)
    selected_categories = st.multiselect(
        "Business Line", list(PRODUCT_CATEGORIES.keys()), default=list(PRODUCT_CATEGORIES.keys())
    )
    products_filter = [p for cat in selected_categories for p in PRODUCT_CATEGORIES.get(cat, [])]

    st.divider()
    st.caption("Mock data · For illustrative purposes only")

# ── Filter clients ─────────────────────────────────────────────────────────────
filtered_clients = [
    c for c in CLIENTS
    if c["sector"] in selected_sectors and c["client_type"] in selected_types
]
all_opps = get_all_opportunities(filtered_clients)
filtered_opps = [
    o for o in all_opps
    if o["score"] >= min_score and o["product"] in products_filter
]

# ── Page tabs ──────────────────────────────────────────────────────────────────
tab_dashboard, tab_pipeline, tab_client = st.tabs([
    "📊 Portfolio Overview", "🎯 Opportunity Pipeline", "🔍 Client Deep Dive"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Portfolio Overview
# ══════════════════════════════════════════════════════════════════════════════
with tab_dashboard:
    st.markdown("### US & International Subsidiary Trade Finance Portfolio")
    st.caption(f"Showing {len(filtered_clients)} clients · {len(filtered_opps)} cross-sell opportunities identified")

    # KPI row
    total_trade_vol = sum(c["trade_volume_usd_m"] for c in filtered_clients)
    total_rev_potential = sum(o["estimated_revenue_usd_k"] for o in filtered_opps) / 1000
    high_priority = sum(1 for o in filtered_opps if o["score"] >= 70)
    avg_products = sum(len(c["current_products"]) for c in filtered_clients) / max(len(filtered_clients), 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trade Volume", f"${total_trade_vol:,.0f}M")
    col2.metric("Cross-Sell Revenue Potential", f"${total_rev_potential:,.1f}M")
    col3.metric("High-Priority Opportunities", f"{high_priority}")
    col4.metric("Avg Products per Client", f"{avg_products:.1f} / {len(GTS_PRODUCTS)}")

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Product penetration heatmap
        st.markdown("#### Product Penetration by Client")
        matrix_data = []
        for c in filtered_clients:
            row = {"Client": c["client"]}
            for p in GTS_PRODUCTS:
                row[p] = 1 if p in c["current_products"] else 0
            matrix_data.append(row)
        df_matrix = pd.DataFrame(matrix_data).set_index("Client")

        fig_heat = px.imshow(
            df_matrix,
            color_continuous_scale=[[0, "#f5f5f5"], [1, "#DB0011"]],
            aspect="auto",
            labels={"color": "Enrolled"},
        )
        fig_heat.update_traces(showscale=False)
        fig_heat.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=380,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_right:
        # Opportunity score distribution by product
        st.markdown("#### Avg Opportunity Score by Product")
        product_scores = {}
        for p in GTS_PRODUCTS:
            scores = [o["score"] for o in filtered_opps if o["product"] == p]
            product_scores[p] = sum(scores) / len(scores) if scores else 0

        df_prod = pd.DataFrame(
            [{"Product": k, "Avg Score": v} for k, v in product_scores.items()]
        ).sort_values("Avg Score", ascending=True)

        fig_bar = px.bar(
            df_prod, x="Avg Score", y="Product", orientation="h",
            color="Avg Score",
            color_continuous_scale=[[0, "#ffcccc"], [0.5, "#ff6666"], [1, "#DB0011"]],
        )
        fig_bar.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=320,
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(range=[0, 100]),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Trade volume vs DSO scatter
        st.markdown("#### Working Capital Positioning")
        df_scatter = get_portfolio_df()
        df_scatter = df_scatter[df_scatter["Sector"].isin(selected_sectors)]
        fig_scatter = px.scatter(
            df_scatter, x="DSO (days)", y="DPO (days)",
            size="Trade Volume ($M)", color="Sector",
            hover_name="Client",
            size_max=30,
        )
        fig_scatter.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=280)
        st.plotly_chart(fig_scatter, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Opportunity Pipeline
# ══════════════════════════════════════════════════════════════════════════════
with tab_pipeline:
    st.markdown("### Cross-Sell Opportunity Pipeline")
    st.caption("Ranked by opportunity score · Estimated revenue is indicative only")

    if not filtered_opps:
        st.info("No opportunities match current filters. Adjust the sidebar filters.")
    else:
        # Summary table
        df_opps = pd.DataFrame([{
            "Client": o["client"],
            "Type": o.get("client_type", ""),
            "HQ": o["hq"],
            "Sector": o["sector"],
            "Product": o["product"],
            "Score": o["score"],
            "Priority": score_label(o["score"]),
            "Est. Revenue ($K)": o["estimated_revenue_usd_k"],
            "Relationship (yrs)": o["relationship_years"],
        } for o in filtered_opps])

        def color_priority(val):
            if val == "High":
                return "background-color: #d4edda; color: #155724; font-weight: bold"
            elif val == "Medium":
                return "background-color: #fff3cd; color: #856404; font-weight: bold"
            return "background-color: #f8f9fa; color: #6c757d"

        styled = df_opps.style.map(color_priority, subset=["Priority"])
        st.dataframe(styled, use_container_width=True, hide_index=True, height=420)

        st.divider()

        # Top 5 detailed cards
        st.markdown("#### Top Priority Actions")
        top5 = [o for o in filtered_opps if o["score"] >= 70][:5]
        if not top5:
            top5 = filtered_opps[:3]

        for opp in top5:
            client_data_opp = next((c for c in CLIENTS if c["client"] == opp["client"]), None)
            with st.expander(
                f"**{opp['client']}** — {opp['product']}  |  Score: {opp['score']}  |  ~${opp['estimated_revenue_usd_k']:,}K",
                expanded=False,
            ):
                c1, c2, c3 = st.columns(3)
                c1.metric("Opportunity Score", f"{opp['score']} / 100")
                c2.metric("Est. Annual Revenue", f"${opp['estimated_revenue_usd_k']:,}K")
                c3.metric("Relationship", f"{opp['relationship_years']} years")

                if client_data_opp:
                    bankers = get_bankers_for_opportunity(client_data_opp, opp["product"])
                    b1, b2 = st.columns(2)
                    rm_name, rm_title = bankers["rm"]
                    b1.markdown(f"**RM:** 👤 {rm_name}  \n_{rm_title}_")
                    if bankers["specialists"]:
                        spec_name, spec_title = bankers["specialists"][0]
                        b2.markdown(f"**Product Specialist:** 👤 {spec_name}  \n_{spec_title}_")

                st.markdown("**Why this opportunity:**")
                for point in opp["rationale"]:
                    st.markdown(f"- {point}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Client Deep Dive
# ══════════════════════════════════════════════════════════════════════════════
with tab_client:
    st.markdown("### Client Deep Dive")

    client_names = [c["client"] for c in filtered_clients]
    selected_name = st.selectbox("Select client", client_names)
    client_data = next(c for c in CLIENTS if c["client"] == selected_name)
    scored = analyze_client(client_data)

    col_info, col_products = st.columns([2, 3])

    with col_info:
        st.markdown(f"#### {client_data['client']}")
        st.markdown(f"**Sector:** {client_data['sector']}  \n**HQ:** {client_data['hq']}  \n**Relationship:** {client_data['relationship_years']} years")
        st.divider()
        m1, m2 = st.columns(2)
        m1.metric("Revenue", f"${client_data['annual_revenue_usd_m']}M")
        m2.metric("Trade Volume", f"${client_data['trade_volume_usd_m']}M")
        m1.metric("DSO", f"{client_data['dso_days']}d")
        m2.metric("DPO", f"{client_data['dpo_days']}d")
        m1.metric("Suppliers", f"{client_data['supplier_count']:,}")
        m2.metric("Trade Geographies", f"{len(client_data['trade_geographies'])}")

        st.markdown("**Trade corridors:**")
        st.markdown("  ".join(f"`{g}`" for g in client_data["trade_geographies"]))

    with col_products:
        st.markdown("#### Product Coverage")
        existing = client_data["current_products"]
        for cat, prods in PRODUCT_CATEGORIES.items():
            st.markdown(f"**{cat}**")
            cols = st.columns(2)
            for i, p in enumerate(prods):
                badge = "✅" if p in existing else "⬜"
                cols[i % 2].markdown(f"{badge} {p.split(' - ', 1)[-1] if ' - ' in p else p}")

        st.divider()
        st.markdown("#### Cross-Sell Opportunity Scores")

        # Horizontal bar chart — 18 products, sorted by score
        df_scored = pd.DataFrame([
            {"Product": s["product"], "Score": s["score"],
             "Category": product_category(s["product"]),
             "Status": "Enrolled" if s["already_enrolled"] else score_label(s["score"])}
            for s in scored
        ]).sort_values("Score")

        color_map = {"Enrolled": "#aaaaaa", "High": "#DB0011", "Medium": "#ff8800", "Low": "#ffccaa"}
        fig_bar = px.bar(
            df_scored, x="Score", y="Product", orientation="h",
            color="Status", color_discrete_map=color_map,
            category_orders={"Status": ["Enrolled", "Low", "Medium", "High"]},
        )
        fig_bar.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            height=460,
            xaxis=dict(range=[0, 100], title="Score"),
            yaxis_title="",
            legend_title="Priority",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
    st.markdown("#### Call Brief — Top Opportunities")
    st.caption("Click any opportunity to see the rationale and the bankers to loop in")

    new_opps = [s for s in scored if not s["already_enrolled"] and s["score"] >= 40]
    new_opps.sort(key=lambda x: x["score"], reverse=True)

    if not new_opps:
        st.info("This client is fully enrolled or no high-confidence opportunities exist above the threshold.")
    else:
        for opp in new_opps[:8]:
            label_color = {"High": "🟢", "Medium": "🟡", "Low": "⚪"}[score_label(opp["score"])]
            with st.expander(
                f"{label_color} **{opp['product']}** — Score {opp['score']}/100  ·  ~${opp['estimated_revenue_usd_k']:,}K",
                expanded=opp["score"] >= 70,
            ):
                bankers = get_bankers_for_opportunity(client_data, opp["product"])

                b_col, r_col = st.columns([1, 1])
                with b_col:
                    st.markdown("**Relationship Manager**")
                    rm_name, rm_title = bankers["rm"]
                    st.markdown(f"👤 **{rm_name}**  \n_{rm_title}_")

                with r_col:
                    st.markdown("**Product Specialist(s)**")
                    for spec_name, spec_title in bankers["specialists"][:2]:
                        st.markdown(f"👤 **{spec_name}**  \n_{spec_title}_")

                st.markdown("---")
                st.markdown("**Why this opportunity:**")
                for point in opp["rationale"]:
                    st.markdown(f"- {point}")

                if opp["score"] >= 70:
                    st.success("**Recommended action:** Schedule intro with product specialist this quarter")
                elif opp["score"] >= 40:
                    st.warning("**Recommended action:** Qualify further in next relationship review")
