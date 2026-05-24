"""
engine.py — Scoring & analytics for the GTS cockpit.

THREE LAYERS (each a talking point in an interview):

1. EXPLAINABLE CROSS-SELL SCORE (0-100)
   Every score is a waterfall of named components, so you can show a hiring
   manager exactly WHY a client scored 82 for Receivables Finance
   ("base 10 + DSO signal 40 + sector fit 15 + intl flag 17") — not a black box.

2. LOOKALIKE PROPENSITY
   P(product | sector, revenue band, DSO band) computed from adoption in the book,
   Laplace-smoothed. Swap the book for real adoption data and the same code yields
   a real propensity model. That is the calibration story.

3. EXPECTED VALUE RANKING
   EV = propensity x revenue. Pipeline ranks by EV, not raw score, answering
   "where should I spend Tuesday." ev_per_effort adds an efficiency view.

Plus PROGRAM HEALTH for live structured facilities — the actual day-job.
"""

from collections import defaultdict

from data import PRODUCTS, STRUCTURED_PRODUCTS, CLIENTS, get_bankers_for_opportunity

# ── Constants ──────────────────────────────────────────────────────────────────

BASE = 10

MARGIN_BY_LINE = {   # illustrative gross margin in bps — NOT real HSBC pricing
    "GPS": 60, "GM": 45, "GTS": 180, "Lending": 140, "IB": 90,
}

EFFORT_BY_LINE = {"GPS": 2, "GM": 2, "GTS": 4, "Lending": 3, "IB": 5}   # RM-days

# ── Helpers ────────────────────────────────────────────────────────────────────

def _intl(c):  return c["client_type"] == "International Subsidiary"
def _rev_b(c): return c["revenue_usd_m"] / 1000.0


def _rev_band(c):
    r = c["revenue_usd_m"]
    return "small" if r < 800 else "mid" if r < 4000 else "large"


def _dso_band(c):
    d = c["dso"]
    return "low" if d < 45 else "mid" if d < 90 else "high"


# ── Per-product scorers ────────────────────────────────────────────────────────
# Each returns (components, revenue_k_month, margin_bps).
# components = [(label, points), ...]; score = clamp(sum(points), 0, 100).

def _score_receivables_finance(c):
    comp = [("Base", BASE)]
    if c["dso"] >= 90:   comp.append(("High DSO (≥90d)", 40))
    elif c["dso"] >= 60: comp.append(("Elevated DSO (≥60d)", 22))
    elif c["dso"] >= 45: comp.append(("Moderate DSO (≥45d)", 10))
    if c["sector"] in ("Industrials", "Automotive", "Metals & Mining", "Chemicals"):
        comp.append(("Working-capital-heavy sector", 15))
    if _intl(c):
        comp.append(("International subsidiary", 8))
    if c["trade_volume_usd_m"] > 1500:
        comp.append(("Large trade volume", 12))
    rev_k = c["trade_volume_usd_m"] * 0.18 * (MARGIN_BY_LINE["GTS"] / 10000) * 1000 / 12
    return comp, round(rev_k, 1), MARGIN_BY_LINE["GTS"]


def _score_supply_chain_finance(c):
    comp = [("Base", BASE)]
    if c["dpo"] >= 60:   comp.append(("High DPO (≥60d)", 35))
    elif c["dpo"] >= 45: comp.append(("Elevated DPO (≥45d)", 18))
    if c["supplier_count"] >= 500:   comp.append(("Large supplier base (≥500)", 22))
    elif c["supplier_count"] >= 200: comp.append(("Mid supplier base (≥200)", 12))
    if c["sector"] in ("Retail", "Consumer Goods", "Food & Beverage", "Automotive"):
        comp.append(("Supply-chain-intensive sector", 15))
    if c["trade_volume_usd_m"] > 1000:
        comp.append(("Large trade volume", 10))
    rev_k = c["trade_volume_usd_m"] * 0.22 * (MARGIN_BY_LINE["GTS"] / 10000) * 1000 / 12
    return comp, round(rev_k, 1), MARGIN_BY_LINE["GTS"]


def _score_gps_liquidity(c):
    comp = [("Base", BASE)]
    if _intl(c):
        comp.append(("Intl subsidiary — cash centralisation need", 35))
    if c["revenue_usd_m"] > 4000:
        comp.append(("Large balance footprint", 20))
    if len(c["trade_corridors"]) >= 3:
        comp.append(("Multi-corridor cash flows", 12))
    rev_k = c["revenue_usd_m"] * 0.02 * (MARGIN_BY_LINE["GPS"] / 10000) * 1000 / 12
    return comp, round(rev_k, 1), MARGIN_BY_LINE["GPS"]


def _score_fx_forward(c):
    comp = [("Base", BASE)]
    if _intl(c):
        comp.append(("FX exposure — intl subsidiary", 28))
    if len(c["trade_corridors"]) >= 2:
        comp.append(("Multi-currency corridors", 22))
    if c["trade_volume_usd_m"] > 800:
        comp.append(("Sizeable cross-border flow", 14))
    rev_k = c["trade_volume_usd_m"] * 0.30 * (MARGIN_BY_LINE["GM"] / 10000) * 1000 / 12
    return comp, round(rev_k, 1), MARGIN_BY_LINE["GM"]


def _score_dcm(c):
    comp = [("Base", BASE)]
    if _rev_b(c) >= 5:
        comp.append(("Revenue ≥$5B — DCM candidate", 45))
    elif _rev_b(c) >= 2:
        comp.append(("Revenue ≥$2B", 22))
    if c["sector"] in ("Energy", "Telecom", "Industrials", "Aerospace & Defense"):
        comp.append(("Capital-intensive sector", 12))
    rev_k = max(c["revenue_usd_m"] * 0.004, 8) * (MARGIN_BY_LINE["IB"] / 10000) * 1000 / 12
    return comp, round(rev_k, 1), MARGIN_BY_LINE["IB"]


def _generic_scorer(line):
    def scorer(c):
        comp = [("Base", BASE)]
        if c["trade_volume_usd_m"] > 1000: comp.append(("Trade volume", 14))
        if _intl(c):                        comp.append(("International subsidiary", 12))
        if c["gov_contracts"] and line == "GTS":
            comp.append(("Government contracts", 18))
        if c["revenue_usd_m"] > 3000:       comp.append(("Scale", 12))
        margin = MARGIN_BY_LINE[line]
        rev_k  = c["trade_volume_usd_m"] * 0.05 * (margin / 10000) * 1000 / 12
        return comp, round(rev_k, 1), margin
    return scorer


SCORERS = {
    "GTS Receivables Finance":  _score_receivables_finance,
    "GTS Supply Chain Finance": _score_supply_chain_finance,
    "GPS Liquidity Management": _score_gps_liquidity,
    "GM FX Spot & Forward":     _score_fx_forward,
    "IB Debt Capital Markets":  _score_dcm,
}
for _p, _line in PRODUCTS.items():
    SCORERS.setdefault(_p, _generic_scorer(_line))


# ── Lookalike propensity ───────────────────────────────────────────────────────

def _build_propensity_table(clients):
    counts = defaultdict(lambda: [0, 0])
    for c in clients:
        kb = (c["sector"], _rev_band(c), _dso_band(c))
        for product in PRODUCTS:
            k = (kb, product)
            counts[k][1] += 1
            if product in c["enrolled"]:
                counts[k][0] += 1
    return {k: (enr + 1) / (tot + 2) for k, (enr, tot) in counts.items()}


_PROPENSITY = _build_propensity_table(CLIENTS)


def propensity(client, product):
    key = ((client["sector"], _rev_band(client), _dso_band(client)), product)
    return _PROPENSITY.get(key, 0.2)


# ── Public scoring API ─────────────────────────────────────────────────────────

def score_label(score):
    return "High" if score >= 70 else "Medium" if score >= 40 else "Low"


def score_product(client, product):
    comp, rev_k, margin = SCORERS[product](client)
    raw   = sum(p for _, p in comp)
    score = max(0, min(100, raw))
    prop  = propensity(client, product)
    ev    = round(prop * rev_k, 1)
    eff   = EFFORT_BY_LINE[PRODUCTS[product]]
    return {
        "client_id":        client["id"],
        "client_name":      client["name"],
        "product":          product,
        "line":             PRODUCTS[product],
        "score":            score,
        "label":            score_label(score),
        "components":       comp,
        "revenue_k_month":  rev_k,
        "margin_bps":       margin,
        "propensity":       round(prop, 3),
        "expected_value_k": ev,
        "effort_days":      eff,
        "ev_per_effort":    round(ev / eff, 2),
        "enrolled":         product in client["enrolled"],
    }


def analyze_client(client):
    out = [score_product(client, p) for p in PRODUCTS if p not in client["enrolled"]]
    out.sort(key=lambda x: x["expected_value_k"], reverse=True)
    return out


def get_all_opportunities(clients, min_score=0):
    flat = []
    for c in clients:
        for opp in analyze_client(c):
            if opp["score"] >= min_score:
                flat.append(opp)
    flat.sort(key=lambda x: x["expected_value_k"], reverse=True)
    return flat


def recommended_action(label):
    return {
        "High":   "Schedule specialist intro this quarter",
        "Medium": "Qualify in next quarterly review",
        "Low":    "Monitor; revisit if working-capital profile shifts",
    }[label]


# ── Program health ─────────────────────────────────────────────────────────────

def program_health(p):
    flags = []
    if p["utilization"] > 1.0:
        flags.append(("Utilization breach", f"{p['utilization']*100:.0f}% of limit drawn", "red"))
    elif p["utilization"] > 0.9:
        flags.append(("Near limit", f"{p['utilization']*100:.0f}% utilized", "amber"))
    if p["days_to_rollover"] < 30:
        flags.append(("Rollover imminent", f"{p['days_to_rollover']}d to renewal", "red"))
    elif p["days_to_rollover"] < 60:
        flags.append(("Rollover approaching", f"{p['days_to_rollover']}d to renewal", "amber"))
    if p["rev_variance_pct"] < -0.10:
        flags.append(("Revenue leakage", f"booked {p['rev_variance_pct']*100:.0f}% vs expected", "red"))
    elif p["rev_variance_pct"] < -0.03:
        flags.append(("Revenue drift", f"{p['rev_variance_pct']*100:.0f}% vs expected", "amber"))
    if p["top_obligor_concentration"] > 0.6:
        flags.append(("Concentration risk", f"top obligor {p['top_obligor_concentration']*100:.0f}%", "amber"))

    if any(f[2] == "red" for f in flags):
        verdict = "Action Required"
    elif flags:
        verdict = "Watch"
    else:
        verdict = "Healthy"
    return {"verdict": verdict, "flags": flags}


def portfolio_program_summary(programs):
    total_limit  = sum(p["limit_usd_m"] for p in programs)
    total_drawn  = sum(p["drawn_usd_m"] for p in programs)
    exp_rev      = sum(p["expected_rev_k_month"] for p in programs)
    booked_rev   = sum(p["booked_rev_k_month"] for p in programs)
    action       = sum(1 for p in programs if program_health(p)["verdict"] == "Action Required")
    watch        = sum(1 for p in programs if program_health(p)["verdict"] == "Watch")
    return {
        "n_programs":      len(programs),
        "total_limit_m":   round(total_limit, 1),
        "total_drawn_m":   round(total_drawn, 1),
        "avg_utilization": round(total_drawn / total_limit, 3) if total_limit else 0,
        "expected_rev_k":  round(exp_rev, 1),
        "booked_rev_k":    round(booked_rev, 1),
        "rev_leakage_k":   round(exp_rev - booked_rev, 1),
        "action_required": action,
        "watch":           watch,
    }
