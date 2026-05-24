"""
ai_brief.py — AI-generated RM call brief.

build_brief_prompt(client, opps) -> str
    Deterministic prompt from the client's working-capital profile and top
    opportunities. Always available — no API key required.

generate_brief(client, opps) -> str
    Calls the Anthropic API. Reads ANTHROPIC_API_KEY from env or st.secrets.
    Falls back gracefully to a templated brief if no key is configured,
    so the deployed app never errors on stage.
"""

import os


def build_brief_prompt(client, opps):
    top   = opps[:3]
    lines = [
        f"Client: {client['name']} ({client['sector']}, {client['segment']}, {client['client_type']})",
        f"HQ: {client['hq']} | Revenue: ${client['revenue_usd_m']/1000:.1f}B | "
        f"Trade volume: ${client['trade_volume_usd_m']/1000:.1f}B",
        f"Working capital: DSO {client['dso']}d, DPO {client['dpo']}d, "
        f"{client['supplier_count']:,} suppliers",
        f"Trade corridors: {', '.join(client['trade_corridors'])}",
        f"Currently enrolled: {', '.join(client['enrolled'])}",
        "",
        "Top expansion opportunities (by expected value):",
    ]
    for o in top:
        why = "; ".join(f"{lbl} (+{pts})" for lbl, pts in o["components"] if lbl != "Base")
        lines.append(
            f"  - {o['product']}: score {o['score']} ({o['label']}), "
            f"propensity {o['propensity']*100:.0f}%, ~${o['revenue_k_month']:.0f}k/mo. "
            f"Drivers: {why}"
        )
    return "\n".join(lines)


_SYSTEM = (
    "You are a trade-finance sales enablement assistant for an HSBC GTS Sales "
    "Program Manager. Given a client's working-capital profile and ranked "
    "cross-sell opportunities, write a concise call brief an RM can use before a "
    "client meeting. Structure: (1) one-line situation, (2) 2-3 talking points "
    "tied to the client's DSO/DPO/supplier dynamics, (3) the single best next "
    "product to lead with and why, (4) one smart discovery question. Be specific "
    "and senior; no fluff, no disclaimers. Under 180 words."
)


def generate_brief(client, opps):
    prompt = build_brief_prompt(client, opps)
    key    = os.environ.get("ANTHROPIC_API_KEY")
    try:
        import streamlit as st
        key = key or st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass

    if not key:
        return _fallback_brief(client, opps)

    try:
        import anthropic
        ac  = anthropic.Anthropic(api_key=key)
        msg = ac.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if b.type == "text")
    except Exception as e:
        return _fallback_brief(client, opps) + f"\n\n_(live API unavailable: {e})_"


def _fallback_brief(client, opps):
    lead = opps[0] if opps else None
    wc   = ("elevated DSO"       if client["dso"] >= 75 else
            "stretched DPO"      if client["dpo"] >= 60 else
            "balanced working capital")
    out  = [
        f"**{client['name']} — call brief**",
        f"Situation: {client['segment']} {client['sector']} name, "
        f"${client['revenue_usd_m']/1000:.1f}B revenue, {wc} "
        f"(DSO {client['dso']}d / DPO {client['dpo']}d).",
    ]
    if lead:
        out.append(
            f"Lead with **{lead['product']}** — propensity {lead['propensity']*100:.0f}%, "
            f"~${lead['revenue_k_month']:.0f}k/mo. Anchor on freeing trapped working capital "
            f"across {client['supplier_count']:,} suppliers and "
            f"{len(client['trade_corridors'])} trade corridors."
        )
        out.append(
            f"Discovery question: how is the treasury team currently financing the "
            f"{client['dso']}-day receivables cycle, and where does that create FX or "
            f"liquidity friction across {client['trade_corridors'][0]}?"
        )
    return "\n\n".join(out)
