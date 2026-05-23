"""
Cross-sell opportunity scoring engine — 18 HSBC product lines.

Each scorer returns:
  score: 0-100
  rationale: list of bullet strings
  estimated_revenue_usd_k: rough annual revenue uplift estimate
"""

from __future__ import annotations
from typing import Any


# ── GTS Products ───────────────────────────────────────────────────────────────

def score_gts_supply_chain_solutions(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GTS - Supply Chain Solutions" in c["current_products"]:
        return {"score": 0, "rationale": ["Already enrolled — assess program expansion to additional supplier tiers"], "estimated_revenue_usd_k": 0}

    if c["dpo_days"] >= 60:
        score += 35
        rationale.append(f"DPO of {c['dpo_days']}d signals suppliers extending credit — SCF converts this into a competitive working capital lever")
    elif c["dpo_days"] >= 45:
        score += 20
        rationale.append(f"DPO of {c['dpo_days']}d indicates moderate supplier payment stretching — SCF can optimize the cash conversion cycle")
    else:
        rationale.append(f"DPO of {c['dpo_days']}d is low — client pays quickly, limiting SCF program economics")

    if c["supplier_count"] >= 400:
        score += 30
        rationale.append(f"Large supplier base ({c['supplier_count']}) creates strong SCF program economics and fee income")
    elif c["supplier_count"] >= 150:
        score += 18
        rationale.append(f"Mid-size supplier base ({c['supplier_count']}) supports a viable SCF program")
    else:
        score += 5
        rationale.append(f"Small supplier base ({c['supplier_count']}) may limit program scale")

    if c["sector"] in {"Retail", "Food & Beverage", "Apparel", "Technology", "Agriculture", "Manufacturing"}:
        score += 20
        rationale.append(f"{c['sector']} sector has well-established supply chain finance adoption patterns")

    if c["seasonal_trade"]:
        score += 10
        rationale.append("Seasonal trade cycles create natural working capital gaps SCF can bridge")

    rev = int(c["trade_volume_usd_m"] * 0.004 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gts_receivables_finance(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GTS - Receivables Finance" in c["current_products"]:
        return {"score": 0, "rationale": ["Already enrolled — review limit utilization and eligibility for new buyer programs"], "estimated_revenue_usd_k": 0}

    if c["dso_days"] >= 90:
        score += 40
        rationale.append(f"DSO of {c['dso_days']}d represents significant tied-up working capital — receivables finance directly accelerates cash conversion")
    elif c["dso_days"] >= 65:
        score += 25
        rationale.append(f"DSO of {c['dso_days']}d above typical benchmark — client would benefit from an accelerated collection program")
    else:
        rationale.append(f"DSO of {c['dso_days']}d is manageable — receivables finance is a lower priority")

    export_count = len([g for g in c["trade_geographies"] if g != "USA"])
    if export_count >= 3:
        score += 25
        rationale.append(f"Active in {export_count} export markets — cross-border receivables create natural demand for purchase/finance programs")
    elif export_count >= 2:
        score += 15
        rationale.append(f"Export activity in {export_count} markets supports a receivables program case")

    if c["sector"] in {"Mining", "Chemicals", "Technology", "Agriculture", "Pharmaceuticals", "Food & Beverage", "Apparel", "Manufacturing"}:
        score += 20
        rationale.append(f"{c['sector']} is a B2B sector with large-ticket, predictable receivables ideal for financing")

    if c["annual_revenue_usd_m"] >= 500:
        score += 15
        rationale.append(f"Revenue scale (${c['annual_revenue_usd_m']}M) justifies operational overhead of a receivables program")

    rev = int(c["dso_days"] * c["trade_volume_usd_m"] * 0.00015 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gts_documentary_trade(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GTS - Documentary Trade" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Documentary Trade — focus on expanding to new trade corridors and standby LCs"], "estimated_revenue_usd_k": 0}

    geo_count = len(c["trade_geographies"])
    if geo_count >= 3:
        score += 35
        rationale.append(f"Trading across {geo_count} geographies creates significant counterparty risk that documentary instruments mitigate")
    elif geo_count >= 2:
        score += 20
        rationale.append(f"Cross-border trade in {geo_count} markets creates documentary trade opportunity")

    if c["sector"] in {"Mining", "Energy", "Chemicals", "Agriculture", "Infrastructure", "Manufacturing"}:
        score += 30
        rationale.append(f"{c['sector']} sector relies on LCs and documentary collections for large cross-border transactions")

    if c["trade_volume_usd_m"] >= 200:
        score += 25
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M justifies a dedicated documentary trade facility")
    elif c["trade_volume_usd_m"] >= 100:
        score += 15
        rationale.append(f"Moderate trade volume (${c['trade_volume_usd_m']}M) supports a documentary trade facility at smaller scale")

    rev = int(c["trade_volume_usd_m"] * 0.003 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gts_trade_loans(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GTS - Trade Loans" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Trade Loans — review for limit expansion, tenor optimization, or new currency tranches"], "estimated_revenue_usd_k": 0}

    if c["trade_volume_usd_m"] >= 500:
        score += 35
        rationale.append(f"High trade volume (${c['trade_volume_usd_m']}M) typically requires pre/post-shipment financing")
    elif c["trade_volume_usd_m"] >= 200:
        score += 20
        rationale.append(f"Significant trade volume (${c['trade_volume_usd_m']}M) creates funding gap trade loans can fill")

    if c["seasonal_trade"]:
        score += 25
        rationale.append("Seasonal trade patterns create predictable financing windows — trade loans are ideal for inventory buildup periods")

    if c["sector"] in {"Mining", "Agriculture", "Energy", "Chemicals", "Infrastructure", "Manufacturing"}:
        score += 25
        rationale.append(f"{c['sector']} sector has long cash conversion cycles that benefit from trade loan facilities")

    if c["annual_revenue_usd_m"] >= 300:
        score += 15
        rationale.append("Revenue scale supports credit appetite for a trade loan facility")

    rev = int(c["trade_volume_usd_m"] * 0.006 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gts_guarantees(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GTS - Guarantees" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Guarantees — assess for additional guarantee types or increased limits"], "estimated_revenue_usd_k": 0}

    if c["government_contracts"]:
        score += 45
        rationale.append("Government contracts mandate performance bonds, bid bonds, and advance payment guarantees — strong product fit")

    if c["sector"] in {"Construction", "Infrastructure", "Energy", "Mining", "Manufacturing"}:
        score += 30
        rationale.append(f"{c['sector']} sector regularly requires tender, performance, and advance payment guarantees")

    if c["trade_volume_usd_m"] >= 200:
        score += 15
        rationale.append("Scale of trade activity increases counterparty demand for bank-backed guarantees")

    if len(c["trade_geographies"]) >= 3:
        score += 10
        rationale.append("Multi-geography presence increases cross-border counterparty risk that guarantees can mitigate")

    rev = int(c["annual_revenue_usd_m"] * 0.001 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gts_cstf(c: dict[str, Any]) -> dict:
    """Commodity-Structured Trade Finance — for commodity-intensive sectors."""
    score = 0
    rationale = []
    if "GTS - CSTF" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using CSTF — review for new commodity lines or structured borrowing base expansion"], "estimated_revenue_usd_k": 0}

    commodity_sectors = {"Mining", "Agriculture", "Energy", "Chemicals", "Food & Beverage"}
    if c["sector"] in commodity_sectors:
        score += 45
        rationale.append(f"{c['sector']} sector is a natural fit for commodity-structured trade finance — inventory and receivables create borrowing base")
    else:
        rationale.append(f"{c['sector']} sector has limited CSTF applicability — commodity collateral is typically absent")
        return {"score": score, "rationale": rationale, "estimated_revenue_usd_k": 0}

    if c["trade_volume_usd_m"] >= 500:
        score += 30
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M supports a structured commodity finance facility with meaningful borrowing base")
    elif c["trade_volume_usd_m"] >= 200:
        score += 18
        rationale.append(f"Moderate commodity trade volume (${c['trade_volume_usd_m']}M) supports a smaller CSTF structure")

    if len([g for g in c["trade_geographies"] if g != "USA"]) >= 2:
        score += 15
        rationale.append("Cross-border commodity flows create natural CSTF structure (prepayment, borrowing base, or tolling)")

    if c["seasonal_trade"]:
        score += 10
        rationale.append("Seasonal commodity cycles create structured finance opportunities around harvest/production windows")

    rev = int(c["trade_volume_usd_m"] * 0.008 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


# ── GPS Products ───────────────────────────────────────────────────────────────

def score_gps_current_accounts(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GPS - Current Accounts" in c["current_products"]:
        return {"score": 0, "rationale": ["Already holds Current Accounts — assess for additional currencies or entity consolidation"], "estimated_revenue_usd_k": 0}

    score += 40
    rationale.append("Operational current accounts are a foundational relationship anchor — prerequisite for most other GPS products")

    if c["client_type"] == "International Subsidiary":
        score += 30
        rationale.append("International subsidiary operating in the US typically requires dedicated USD current account infrastructure — natural HSBC fit given global network")

    if c["multi_currency"]:
        score += 20
        rationale.append("Multi-currency trading activity requires currency-specific account structures — opportunity for multi-currency current account setup")

    if len(c["trade_geographies"]) >= 3:
        score += 10
        rationale.append(f"Operating across {len(c['trade_geographies'])} markets increases need for organized account structures by currency/entity")

    rev = int(c["annual_revenue_usd_m"] * 0.0005 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gps_savings_deposits(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GPS - Savings & Deposits" in c["current_products"]:
        return {"score": 0, "rationale": ["Already holding Savings & Deposits — review rate optimization and tenor laddering"], "estimated_revenue_usd_k": 0}

    if c["annual_revenue_usd_m"] >= 1000:
        score += 35
        rationale.append(f"Large corporate (${c['annual_revenue_usd_m']}M revenue) typically carries excess operating cash suitable for deposit products")
    elif c["annual_revenue_usd_m"] >= 400:
        score += 20
        rationale.append(f"Mid-size corporate (${c['annual_revenue_usd_m']}M revenue) likely holds short-term cash suitable for HSBC deposit programs")

    if c["sector"] in {"Energy", "Mining", "Technology", "Pharmaceuticals"}:
        score += 25
        rationale.append(f"{c['sector']} companies often carry significant cash balances between capital deployments — deposit programs capture this")

    if c["government_contracts"]:
        score += 20
        rationale.append("Government contract milestones create lumpy cash receipts — deposit products optimize yield on interim balances")

    if c["relationship_years"] >= 5:
        score += 20
        rationale.append(f"{c['relationship_years']}-year relationship provides trust and wallet visibility needed to win deposit mandates")

    rev = int(c["annual_revenue_usd_m"] * 0.001 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gps_term_deposits(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GPS - Term Deposits" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Term Deposits — review maturity profile and propose rate optimization"], "estimated_revenue_usd_k": 0}

    if c["annual_revenue_usd_m"] >= 2000:
        score += 40
        rationale.append(f"Large corporate scale (${c['annual_revenue_usd_m']}M revenue) generates surplus cash suitable for fixed-term placement")
    elif c["annual_revenue_usd_m"] >= 800:
        score += 25
        rationale.append(f"Revenue of ${c['annual_revenue_usd_m']}M supports predictable cash surpluses for term placement")

    if c["seasonal_trade"]:
        score += 25
        rationale.append("Seasonal trade creates predictable off-peak cash surpluses — term deposits optimize yield during low-activity periods")

    if c["sector"] in {"Energy", "Mining", "Agriculture", "Pharmaceuticals", "Technology"}:
        score += 20
        rationale.append(f"{c['sector']} companies often generate significant operating cash flow between investment cycles")

    if c["relationship_years"] >= 4:
        score += 15
        rationale.append(f"Established {c['relationship_years']}-year relationship provides the trust required for term deposit mandates")

    rev = int(c["annual_revenue_usd_m"] * 0.0015 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gps_liquidity_channel(c: dict[str, Any]) -> dict:
    """GPS Liquidity & Channel — cash pooling, notional pooling, treasury management."""
    score = 0
    rationale = []
    if "GPS - Liquidity & Channel" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Liquidity & Channel — assess for additional entities or cross-currency pooling structures"], "estimated_revenue_usd_k": 0}

    if c["client_type"] == "International Subsidiary":
        score += 35
        rationale.append("International subsidiary structure creates natural demand for cross-border notional pooling — HSBC's global network is a key differentiator here")

    if c["annual_revenue_usd_m"] >= 1000:
        score += 25
        rationale.append(f"Corporate scale (${c['annual_revenue_usd_m']}M revenue) justifies a dedicated liquidity management structure")

    if c["multi_currency"]:
        score += 20
        rationale.append("Multi-currency operations create idle currency balances — liquidity pooling consolidates these for better yield and reduced FX drag")

    if len(c["trade_geographies"]) >= 3:
        score += 15
        rationale.append(f"Presence in {len(c['trade_geographies'])} markets creates fragmented cash positions that pooling can consolidate")

    if c["seasonal_trade"]:
        score += 5
        rationale.append("Seasonal cash flow patterns benefit from dynamic liquidity structures that shift balances automatically")

    rev = int(c["annual_revenue_usd_m"] * 0.0008 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gps_international_payments(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GPS - International Payments" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using International Payments — review for new corridors and straight-through processing improvements"], "estimated_revenue_usd_k": 0}

    intl_geos = len([g for g in c["trade_geographies"] if g != "USA"])
    if intl_geos >= 4:
        score += 40
        rationale.append(f"Active cross-border payments to {intl_geos} markets — HSBC's global network delivers competitive pricing and faster settlement")
    elif intl_geos >= 2:
        score += 25
        rationale.append(f"International payments to {intl_geos} markets — strong case for routing through HSBC's network")

    if c["client_type"] == "International Subsidiary":
        score += 25
        rationale.append("Subsidiary payments to parent and sister entities are a natural, high-volume use case for HSBC's intercompany payment rails")

    if c["multi_currency"]:
        score += 20
        rationale.append("Multi-currency operations require reliable cross-currency payment execution — HSBC's FX-embedded payment capability is a differentiator")

    if c["trade_volume_usd_m"] >= 300:
        score += 15
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M generates significant cross-border payment flows with meaningful fee opportunity")

    rev = int(c["trade_volume_usd_m"] * 0.003 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gps_domestic_payments(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GPS - Domestic Payments" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Domestic Payments — review for digital channel migration and straight-through processing"], "estimated_revenue_usd_k": 0}

    score += 30
    rationale.append("Domestic ACH, wires, and check replacement are foundational payment services — high attach rate for operating companies")

    if c["supplier_count"] >= 200:
        score += 25
        rationale.append(f"Large supplier base ({c['supplier_count']}) drives high domestic payment volumes — strong candidate for batch payment automation")

    if c["sector"] in {"Retail", "Food & Beverage", "Manufacturing", "Construction", "Agriculture"}:
        score += 25
        rationale.append(f"{c['sector']} sector has dense domestic supplier/customer payment networks — high payment volume opportunity")

    if c["annual_revenue_usd_m"] >= 500:
        score += 20
        rationale.append(f"Scale (${c['annual_revenue_usd_m']}M revenue) generates significant domestic payment flows worth capturing")

    rev = int(c["annual_revenue_usd_m"] * 0.0003 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gps_cards(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GPS - Cards" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using Cards — assess for virtual card expansion and rebate program optimization"], "estimated_revenue_usd_k": 0}

    if c["annual_revenue_usd_m"] >= 500:
        score += 30
        rationale.append(f"Corporate of ${c['annual_revenue_usd_m']}M revenue typically has significant T&E and procurement card spend")

    if c["supplier_count"] >= 100:
        score += 25
        rationale.append(f"Large supplier base ({c['supplier_count']}) creates procurement card opportunity — virtual cards can replace lower-value supplier payments")

    if c["sector"] in {"Technology", "Pharmaceuticals", "Retail", "Manufacturing", "Energy"}:
        score += 20
        rationale.append(f"{c['sector']} sector has high T&E and procurement card spend typical of white-collar / distributed workforces")

    if c["multi_currency"]:
        score += 15
        rationale.append("Multi-currency operations create demand for corporate cards with FX transparency and international acceptance")

    if len(c["trade_geographies"]) >= 3:
        score += 10
        rationale.append(f"Operating across {len(c['trade_geographies'])} markets creates multi-country card program opportunity")

    rev = int(c["annual_revenue_usd_m"] * 0.0004 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


# ── Global Markets Products ────────────────────────────────────────────────────

def score_gm_forex_cash(c: dict[str, Any]) -> dict:
    """GM Forex Cash — spot FX, FX forwards, vanilla FX risk management."""
    score = 0
    rationale = []
    if "GM - Forex - Cash" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using GM Forex Cash — review hedging ratio and propose program expansion to new currency pairs"], "estimated_revenue_usd_k": 0}

    if not c["multi_currency"]:
        return {"score": 5, "rationale": ["Single-currency operations limit FX risk management need"], "estimated_revenue_usd_k": 0}

    score += 40
    rationale.append("Multi-currency trade exposure creates natural FX risk that spot and forward hedging can manage")

    geo_count = len(c["trade_geographies"])
    if geo_count >= 4:
        score += 30
        rationale.append(f"Presence in {geo_count} markets means exposure to multiple currency pairs — structured FX cash program is warranted")
    elif geo_count >= 3:
        score += 20
        rationale.append(f"Operations across {geo_count} geographies create meaningful multi-currency exposure")

    if c["sector"] in {"Mining", "Agriculture", "Energy", "Manufacturing"}:
        score += 20
        rationale.append(f"{c['sector']} sector faces commodity-linked FX volatility — spot and forward hedging are strategic risk management tools")

    if c["trade_volume_usd_m"] >= 300:
        score += 10
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M makes unhedged FX exposure material to earnings")

    rev = int(c["trade_volume_usd_m"] * 0.002 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gm_forex_tfx(c: dict[str, Any]) -> dict:
    """GM FOREX TFX — transactional FX embedded in payment and trade flows."""
    score = 0
    rationale = []
    if "GM - FOREX - TFX" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using TFX — review automation coverage and propose API integration for straight-through FX conversion"], "estimated_revenue_usd_k": 0}

    if not c["multi_currency"]:
        return {"score": 5, "rationale": ["Predominantly single-currency — TFX applicability is limited"], "estimated_revenue_usd_k": 0}

    intl_geos = len([g for g in c["trade_geographies"] if g != "USA"])
    if intl_geos >= 3:
        score += 40
        rationale.append(f"High-frequency cross-border payments to {intl_geos} markets create significant transactional FX conversion volume — TFX automates this at scale")
    elif intl_geos >= 2:
        score += 25
        rationale.append(f"Cross-border payment flows to {intl_geos} markets support TFX automation case")

    if c["trade_volume_usd_m"] >= 400:
        score += 30
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M generates high-frequency FX conversion transactions — TFX delivers cost savings vs. manual spot desk execution")
    elif c["trade_volume_usd_m"] >= 150:
        score += 18
        rationale.append(f"Moderate trade volume (${c['trade_volume_usd_m']}M) supports a TFX automation business case")

    if c["client_type"] == "International Subsidiary":
        score += 20
        rationale.append("Intercompany settlement flows between subsidiary and parent create regular, predictable FX conversion — ideal for TFX automation")

    if c["sector"] in {"Technology", "Pharmaceuticals", "Retail", "Apparel"}:
        score += 10
        rationale.append(f"{c['sector']} sector has high-frequency cross-border payment patterns well-suited to automated FX conversion")

    rev = int(c["trade_volume_usd_m"] * 0.0025 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


def score_gm_futures(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "GM - Futures" in c["current_products"]:
        return {"score": 0, "rationale": ["Already using GM Futures — review hedging strategy and propose options or structured solutions"], "estimated_revenue_usd_k": 0}

    commodity_sectors = {"Mining", "Agriculture", "Energy", "Chemicals", "Food & Beverage"}
    if c["sector"] in commodity_sectors:
        score += 45
        rationale.append(f"{c['sector']} sector has direct commodity price exposure — futures hedging is a core treasury risk management tool")
    elif c["multi_currency"]:
        score += 20
        rationale.append("Multi-currency exposure creates FX futures hedging opportunity alongside commodity price risk management")
    else:
        return {"score": 5, "rationale": ["Limited commodity or FX exposure — futures hedging need is low"], "estimated_revenue_usd_k": 0}

    if c["trade_volume_usd_m"] >= 500:
        score += 25
        rationale.append(f"Trade volume of ${c['trade_volume_usd_m']}M creates material price exposure that warrants an exchange-traded futures hedging program")
    elif c["trade_volume_usd_m"] >= 200:
        score += 15
        rationale.append(f"Commodity trade volume of ${c['trade_volume_usd_m']}M supports a futures program at smaller scale")

    if c["seasonal_trade"]:
        score += 20
        rationale.append("Seasonal production/trade cycles create predictable commodity price windows — futures allow locking in margins in advance")

    if c["annual_revenue_usd_m"] >= 1000:
        score += 10
        rationale.append("Scale supports a dedicated commodity risk management desk conversation")

    rev = int(c["trade_volume_usd_m"] * 0.003 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


# ── Lending ────────────────────────────────────────────────────────────────────

def score_lending_corporate(c: dict[str, Any]) -> dict:
    score = 0
    rationale = []
    if "Lending - Corporate Lending" in c["current_products"]:
        return {"score": 0, "rationale": ["Already in Corporate Lending — assess for facility expansion, term extension, or additional tranches"], "estimated_revenue_usd_k": 0}

    if c["annual_revenue_usd_m"] >= 2000:
        score += 35
        rationale.append(f"Large corporate (${c['annual_revenue_usd_m']}M revenue) has borrowing needs for capex, M&A, or working capital that a revolving credit facility can serve")
    elif c["annual_revenue_usd_m"] >= 500:
        score += 20
        rationale.append(f"Mid-market corporate (${c['annual_revenue_usd_m']}M revenue) typically has RCF or term loan needs — strong lending opportunity")

    if c["government_contracts"]:
        score += 20
        rationale.append("Government contract pipeline provides predictable cash flows — strong basis for credit underwriting")

    if c["sector"] in {"Energy", "Mining", "Infrastructure", "Manufacturing", "Construction"}:
        score += 25
        rationale.append(f"{c['sector']} sector is capital-intensive with regular capex funding needs — corporate lending is a core relationship product")

    if c["relationship_years"] >= 5:
        score += 20
        rationale.append(f"{c['relationship_years']}-year relationship provides financial history and trust needed to structure a credit facility")

    rev = int(c["annual_revenue_usd_m"] * 0.002 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


# ── Investment Banking ─────────────────────────────────────────────────────────

def score_ib_dcm_ig(c: dict[str, Any]) -> dict:
    """IB DCM IG — Investment Grade Debt Capital Markets (bonds, MTNs)."""
    score = 0
    rationale = []
    if "IB - DCM IG" in c["current_products"]:
        return {"score": 0, "rationale": ["Already an IB DCM client — monitor for new issuance windows, liability management, and cross-currency bond opportunities"], "estimated_revenue_usd_k": 0}

    if c["annual_revenue_usd_m"] >= 5000:
        score += 45
        rationale.append(f"Large corporate (${c['annual_revenue_usd_m']}M revenue) is a natural investment grade bond issuer — HSBC as bookrunner or co-manager")
    elif c["annual_revenue_usd_m"] >= 2000:
        score += 28
        rationale.append(f"Revenue of ${c['annual_revenue_usd_m']}M puts client in IG bond market territory — HSBC can compete for lead-left mandate")
    else:
        rationale.append(f"Revenue of ${c['annual_revenue_usd_m']}M is below typical IG bond issuer threshold — DCM opportunity limited at current scale")

    if c["client_type"] == "International Subsidiary":
        score += 25
        rationale.append("International subsidiary of large parent group — parent entity may use HSBC for multi-currency bond issuance; subsidiary relationship supports mandate")

    if c["sector"] in {"Energy", "Infrastructure", "Mining", "Pharmaceuticals", "Technology", "Manufacturing"}:
        score += 15
        rationale.append(f"{c['sector']} sector companies regularly access debt capital markets for capex and refinancing")

    if c["government_contracts"]:
        score += 15
        rationale.append("Government contract revenue base supports investment grade credit profile — favorable for bond market access")

    rev = int(c["annual_revenue_usd_m"] * 0.004 * 1000)
    return {"score": min(score, 100), "rationale": rationale, "estimated_revenue_usd_k": rev}


# ── SCORERS registry ───────────────────────────────────────────────────────────

SCORERS = {
    "GPS - Current Accounts":       score_gps_current_accounts,
    "GPS - Savings & Deposits":     score_gps_savings_deposits,
    "GPS - Term Deposits":          score_gps_term_deposits,
    "GPS - Liquidity & Channel":    score_gps_liquidity_channel,
    "GPS - International Payments": score_gps_international_payments,
    "GPS - Domestic Payments":      score_gps_domestic_payments,
    "GPS - Cards":                  score_gps_cards,
    "GM - Forex - Cash":            score_gm_forex_cash,
    "GM - FOREX - TFX":             score_gm_forex_tfx,
    "GM - Futures":                 score_gm_futures,
    "GTS - Supply Chain Solutions": score_gts_supply_chain_solutions,
    "GTS - Receivables Finance":    score_gts_receivables_finance,
    "GTS - Documentary Trade":      score_gts_documentary_trade,
    "GTS - Trade Loans":            score_gts_trade_loans,
    "GTS - Guarantees":             score_gts_guarantees,
    "GTS - CSTF":                   score_gts_cstf,
    "Lending - Corporate Lending":  score_lending_corporate,
    "IB - DCM IG":                  score_ib_dcm_ig,
}


def analyze_client(c: dict[str, Any]) -> list[dict]:
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
    return "Low"


def product_category(product: str) -> str:
    if product.startswith("GTS"):
        return "GTS"
    if product.startswith("GPS"):
        return "GPS"
    if product.startswith("GM"):
        return "GM"
    if product.startswith("IB"):
        return "IB"
    if product.startswith("Lending"):
        return "Lending"
    return "Other"
