"""
Cross-sell opportunity scoring engine for GTS products.

Each scorer returns a dict with:
  score: 0-100
  rationale: list of bullet strings
  estimated_revenue_usd_k: rough annual revenue uplift estimate
"""

from __future__ import annotations
from typing import Any


def score_supply_chain_finance(c: dict[str, Any]) -> dict:
    """High opportunity when: high DPO (supplier leverage), large supplier base, manufacturing/retail sectors."""
    score = 0
    rationale = []

    if c["dpo_days"] >= 60:
        score += 35
        rationale.append(f"DPO of {c['dpo_days']}d signals suppliers already extending credit — SCF converts this to a competitive advantage")
    elif c["dpo_days"] >= 45:
        score += 20
        rationale.append(f"DPO of {c['dpo_days']}d indicates moderate supplier payment stretching — SCF can optimize working capital")
    else:
        rationale.append(f"DPO of {c['dpo_days']}d is low — client pays suppliers quickly, limiting SCF appeal")

    if c["supplier_count"] >= 400:
        score += 30
        rationale.append(f"Large supplier network ({c['supplier_count']} suppliers) creates strong SCF program economics")
    elif c["supplier_count"] >= 150:
        score += 18
        rationale.append(f"Mid-size supplier base ({c['supplier_count']} suppliers) supports a viable SCF program")
    else:
        score += 5
        rationale.append(f"Small supplier base ({c['supplier_count']} suppliers) may limit program scale")

    favorable_sectors = {"Retail", "Food & Beverage", "Apparel", "Technology", "Agriculture"}
    if c["sector"] in favorable_sectors:
        score += 20
        rationale.append(f"{c['sector']} sector has well-established SCF adoption patterns")

    if c["seasonal_trade"]:
        score += 10
        rationale.append("Seasonal trade cycles create natural working capital gaps SCF can bridge")

    if "Supply Chain Finance" in c["current_products"]:
        score = 0
        rationale = ["Client already enrolled in Supply Chain Finance program"]

    rev_est = int(c["trade_volume_usd_m"] * 0.004 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev_est}


def score_receivables_purchase(c: dict[str, Any]) -> dict:
    """High opportunity when: high DSO, export-heavy, B2B sectors."""
    score = 0
    rationale = []

    if c["dso_days"] >= 90:
        score += 40
        rationale.append(f"DSO of {c['dso_days']}d represents significant tied-up working capital — receivables purchase directly addresses this")
    elif c["dso_days"] >= 65:
        score += 25
        rationale.append(f"DSO of {c['dso_days']}d above sector average — client would benefit from accelerated cash conversion")
    else:
        rationale.append(f"DSO of {c['dso_days']}d is manageable — receivables purchase is a lower priority")

    export_geographies = len([g for g in c["trade_geographies"] if g != c["hq"]])
    if export_geographies >= 3:
        score += 25
        rationale.append(f"Active in {export_geographies} export markets — cross-border receivables create natural demand for purchase programs")
    elif export_geographies >= 2:
        score += 15
        rationale.append(f"Export activity across {export_geographies} markets supports receivables program case")

    b2b_sectors = {"Mining", "Chemicals", "Technology", "Agriculture", "Pharmaceuticals", "Food & Beverage", "Apparel"}
    if c["sector"] in b2b_sectors:
        score += 20
        rationale.append(f"{c['sector']} is a B2B sector with predictable, large-ticket receivables ideal for purchase programs")

    if c["annual_revenue_usd_m"] >= 500:
        score += 15
        rationale.append(f"Scale (${c['annual_revenue_usd_m']}M revenue) justifies the operational overhead of a receivables program")

    if "Receivables Purchase" in c["current_products"]:
        score = 0
        rationale = ["Client already enrolled in Receivables Purchase program"]

    rev_est = int(c["dso_days"] * c["trade_volume_usd_m"] * 0.00015 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev_est}


def score_documentary_credits(c: dict[str, Any]) -> dict:
    """High opportunity when: new import markets, high trade volume, no existing LC facility."""
    score = 0
    rationale = []

    if "Documentary Credits" in c["current_products"]:
        score = 0
        rationale = ["Client already using Documentary Credits — focus on program expansion to new corridors"]
        return {"score": score, "rationale": rationale, "estimated_revenue_usd_k": 0}

    import_geographies = len(c["trade_geographies"])
    if import_geographies >= 3:
        score += 35
        rationale.append(f"Trading across {import_geographies} geographies creates significant counterparty risk that LCs mitigate")
    elif import_geographies >= 2:
        score += 20
        rationale.append(f"Cross-border trade across {import_geographies} markets creates LC opportunity")

    high_lc_sectors = {"Mining", "Energy", "Chemicals", "Agriculture", "Infrastructure"}
    if c["sector"] in high_lc_sectors:
        score += 30
        rationale.append(f"{c['sector']} sector traditionally relies on LCs for large-ticket cross-border transactions")

    if c["trade_volume_usd_m"] >= 200:
        score += 25
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M justifies a dedicated LC facility")
    elif c["trade_volume_usd_m"] >= 100:
        score += 15
        rationale.append(f"Moderate trade volume (${c['trade_volume_usd_m']}M) supports LC facility at smaller scale")

    rev_est = int(c["trade_volume_usd_m"] * 0.003 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev_est}


def score_trade_loans(c: dict[str, Any]) -> dict:
    """High opportunity when: large trade volumes, seasonal needs, not already using."""
    score = 0
    rationale = []

    if "Trade Loans" in c["current_products"]:
        score = 0
        rationale = ["Client already using Trade Loans — review for limit expansion or tenor optimization"]
        return {"score": score, "rationale": rationale, "estimated_revenue_usd_k": 0}

    if c["trade_volume_usd_m"] >= 500:
        score += 35
        rationale.append(f"High trade volume (${c['trade_volume_usd_m']}M) typically requires pre/post-shipment financing")
    elif c["trade_volume_usd_m"] >= 200:
        score += 20
        rationale.append(f"Significant trade volume (${c['trade_volume_usd_m']}M) creates funding gap trade loans can fill")

    if c["seasonal_trade"]:
        score += 25
        rationale.append("Seasonal trade patterns create predictable financing windows — trade loans ideal for inventory buildup periods")

    capital_intensive = {"Mining", "Agriculture", "Energy", "Chemicals", "Infrastructure"}
    if c["sector"] in capital_intensive:
        score += 25
        rationale.append(f"{c['sector']} sector has long cash conversion cycles that benefit from trade loan facilities")

    if c["annual_revenue_usd_m"] >= 300:
        score += 15
        rationale.append("Revenue scale supports credit appetite for a trade loan facility")

    rev_est = int(c["trade_volume_usd_m"] * 0.006 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev_est}


def score_fx_hedging(c: dict[str, Any]) -> dict:
    """High opportunity when: multi-currency exposure, no existing hedging."""
    score = 0
    rationale = []

    if "FX Hedging" in c["current_products"]:
        score = 0
        rationale = ["Client already using FX Hedging — review for coverage ratio and new currency corridors"]
        return {"score": score, "rationale": rationale, "estimated_revenue_usd_k": 0}

    if not c["multi_currency"]:
        rationale.append("Client operates primarily in single currency — FX hedging need is limited")
        return {"score": 5, "rationale": rationale, "estimated_revenue_usd_k": 0}

    score += 40
    rationale.append("Multi-currency trade exposure creates natural FX risk that structured hedging can reduce")

    geo_count = len(c["trade_geographies"])
    if geo_count >= 4:
        score += 30
        rationale.append(f"Presence in {geo_count} markets means exposure to multiple currency pairs — complex hedging program opportunity")
    elif geo_count >= 3:
        score += 20
        rationale.append(f"Operations across {geo_count} geographies create meaningful currency exposure")

    volatile_sectors = {"Mining", "Agriculture", "Energy"}
    if c["sector"] in volatile_sectors:
        score += 20
        rationale.append(f"{c['sector']} sector faces commodity-linked FX volatility — hedging is a strategic need, not just preference")

    if c["trade_volume_usd_m"] >= 300:
        score += 10
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M makes unhedged FX exposure material to earnings")

    rev_est = int(c["trade_volume_usd_m"] * 0.002 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev_est}


def score_bank_guarantees(c: dict[str, Any]) -> dict:
    """High opportunity when: government contracts, project finance, infrastructure."""
    score = 0
    rationale = []

    if "Bank Guarantees" in c["current_products"]:
        score = 0
        rationale = ["Client already using Bank Guarantees — assess for additional guarantee types or increased limits"]
        return {"score": score, "rationale": rationale, "estimated_revenue_usd_k": 0}

    if c["government_contracts"]:
        score += 45
        rationale.append("Government contracts typically mandate performance bonds and bid guarantees — strong product fit")

    guarantee_sectors = {"Construction", "Infrastructure", "Energy", "Mining"}
    if c["sector"] in guarantee_sectors:
        score += 30
        rationale.append(f"{c['sector']} sector regularly requires tender, performance, and advance payment guarantees")

    if c["trade_volume_usd_m"] >= 200:
        score += 15
        rationale.append("Scale of trade activity increases likelihood of counterparties requiring bank guarantees")

    if len(c["trade_geographies"]) >= 3:
        score += 10
        rationale.append("Multi-geography presence increases cross-border counterparty risk that guarantees can mitigate")

    rev_est = int(c["annual_revenue_usd_m"] * 0.001 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev_est}


SCORERS = {
    "Supply Chain Finance": score_supply_chain_finance,
    "Receivables Purchase": score_receivables_purchase,
    "Documentary Credits": score_documentary_credits,
    "Trade Loans": score_trade_loans,
    "FX Hedging": score_fx_hedging,
    "Bank Guarantees": score_bank_guarantees,
}


def analyze_client(c: dict[str, Any]) -> list[dict]:
    """Return scored opportunities for a client, sorted by score desc."""
    results = []
    for product, scorer in SCORERS.items():
        result = scorer(c)
        already_has = product in c["current_products"]
        results.append({
            "product": product,
            "score": result["score"],
            "rationale": result["rationale"],
            "estimated_revenue_usd_k": result["estimated_revenue_usd_k"],
            "already_enrolled": already_has,
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_all_opportunities(clients: list[dict[str, Any]]) -> list[dict]:
    """Flatten all cross-sell opportunities across the portfolio."""
    all_opps = []
    for c in clients:
        scored = analyze_client(c)
        for opp in scored:
            if not opp["already_enrolled"] and opp["score"] > 0:
                all_opps.append({
                    "client": c["client"],
                    "sector": c["sector"],
                    "hq": c["hq"],
                    "client_type": c.get("client_type", "US Domestic"),
                    "product": opp["product"],
                    "score": opp["score"],
                    "estimated_revenue_usd_k": opp["estimated_revenue_usd_k"],
                    "rationale": opp["rationale"],
                    "relationship_years": c["relationship_years"],
                })
    all_opps.sort(key=lambda x: (x["score"], x["estimated_revenue_usd_k"]), reverse=True)
    return all_opps


def score_label(score: int) -> str:
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"
