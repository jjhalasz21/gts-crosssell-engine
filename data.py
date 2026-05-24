"""
data.py — Mock data for the GTS Structured Trade Program Cockpit.

Reframed from a pure cross-sell book into a program-management data model,
matching the Sales Program Manager (GTS) role: proactively managing live
Structured Trade Finance programs (RF / SCF) for GNB and IMM clients,
while still surfacing cross-sell expansion.

Key entities:
  CLIENTS     — the corporate book (GNB + IMM segmentation)
  PRODUCTS    — 18 GTS products across 5 business lines
  PROGRAMS    — live structured trade facilities per client
  SUPPLIERS   — supplier onboarding funnel for each SCF program
  CASES       — open issues requiring stakeholder mobilisation
  RELATIONSHIP_MANAGERS / PRODUCT_SPECIALISTS — the internal cast
"""

import random
from datetime import date, timedelta

SEED  = 42
AS_OF = date(2026, 5, 24)   # single source of truth for "today"

# ── Reference data ─────────────────────────────────────────────────────────────

SECTORS = [
    "Industrials", "Consumer Goods", "Technology", "Healthcare", "Energy",
    "Automotive", "Retail", "Chemicals", "Aerospace & Defense",
    "Metals & Mining", "Telecom", "Food & Beverage", "Pharmaceuticals",
]

SEGMENTS = ["GNB", "IMM"]   # Global Network Banking, International Middle Market

HQ_COUNTRIES_INTL = [
    "Germany", "Japan", "United Kingdom", "France", "South Korea",
    "Netherlands", "Switzerland", "Canada", "Mexico", "Brazil",
    "India", "Singapore", "Italy", "Sweden", "Spain",
]
US_STATES = ["NY", "NJ", "CT", "TX", "CA", "IL", "MA", "OH", "GA", "NC", "WA", "FL"]

TRADE_CORRIDORS = [
    "US-China", "US-EU", "US-Mexico", "US-Japan", "US-Korea", "US-India",
    "US-Brazil", "US-UK", "US-Canada", "US-Vietnam", "US-Germany", "US-LatAm",
]

PRODUCTS = {
    # Global Payments Solutions
    "GPS Liquidity Management":     "GPS",
    "GPS Cross-Border Payments":    "GPS",
    "GPS Virtual Accounts":         "GPS",
    "GPS Commercial Cards":         "GPS",
    # Global Markets
    "GM FX Spot & Forward":         "GM",
    "GM FX Options":                "GM",
    "GM Rates Hedging":             "GM",
    # Global Trade Solutions — heart of this role
    "GTS Receivables Finance":      "GTS",
    "GTS Supply Chain Finance":     "GTS",
    "GTS Documentary Credits":      "GTS",
    "GTS Guarantees & SBLC":        "GTS",
    "GTS Import/Export Loans":      "GTS",
    "GTS Structured Trade Finance": "GTS",
    # Lending
    "Lending Revolving Credit":     "Lending",
    "Lending Term Loan":            "Lending",
    "Lending Asset-Based Lending":  "Lending",
    # Investment Banking
    "IB Debt Capital Markets":      "IB",
    "IB M&A Advisory":              "IB",
}

BUSINESS_LINES = ["GPS", "GM", "GTS", "Lending", "IB"]

STRUCTURED_PRODUCTS = ["GTS Receivables Finance", "GTS Supply Chain Finance"]

# ── Internal bankers ───────────────────────────────────────────────────────────

RELATIONSHIP_MANAGERS = {
    "Industrials":         [("Priya Raman", "Senior RM, GNB"), ("Tom Fletcher", "RM, IMM"), ("Lena Vogt", "RM, GNB")],
    "Consumer Goods":      [("Marco Bianchi", "Senior RM, GNB"), ("Dana Cho", "RM, IMM"), ("Will Hartley", "RM, GNB")],
    "Technology":          [("Aisha Khan", "Senior RM, IMM"), ("Ben Ortiz", "RM, GNB"), ("Sara Lindqvist", "RM, IMM")],
    "Healthcare":          [("Grace Mwangi", "Senior RM, GNB"), ("Paolo Russo", "RM, IMM"), ("Henry Wu", "RM, GNB")],
    "Energy":              [("Olu Adeyemi", "Senior RM, GNB"), ("Kate Sullivan", "RM, IMM"), ("Dmitri Volkov", "RM, GNB")],
    "Automotive":          [("Yuki Tanaka", "Senior RM, GNB"), ("Erik Brandt", "RM, IMM"), ("Nadia Haddad", "RM, GNB")],
    "Retail":              [("Sophie Laurent", "Senior RM, IMM"), ("Raj Malhotra", "RM, GNB"), ("Tessa Boone", "RM, IMM")],
    "Chemicals":           [("Hans Becker", "Senior RM, GNB"), ("Ivy Chen", "RM, IMM"), ("Pablo Mendez", "RM, GNB")],
    "Aerospace & Defense": [("Claire Dubois", "Senior RM, GNB"), ("Sam Whitaker", "RM, IMM"), ("Mei Ling", "RM, GNB")],
    "Metals & Mining":     [("Diego Castro", "Senior RM, GNB"), ("Anna Kowalski", "RM, IMM"), ("Joel Fischer", "RM, GNB")],
    "Telecom":             [("Farah Nasser", "Senior RM, IMM"), ("Greg Olsen", "RM, GNB"), ("Lucia Rossi", "RM, IMM")],
    "Food & Beverage":     [("Tomas Berg", "Senior RM, GNB"), ("Hana Park", "RM, IMM"), ("Owen Reilly", "RM, GNB")],
    "Pharmaceuticals":     [("Nina Petrova", "Senior RM, GNB"), ("Carlos Vega", "RM, IMM"), ("Amara Singh", "RM, GNB")],
}

PRODUCT_SPECIALISTS = {
    "GPS Liquidity Management":     [("Ravi Iyer", "GPS Liquidity Specialist")],
    "GPS Cross-Border Payments":    [("Mona Eltahir", "GPS Payments Specialist")],
    "GPS Virtual Accounts":         [("Derek Lin", "GPS VA Specialist")],
    "GPS Commercial Cards":         [("Cara Nolan", "Commercial Cards Specialist")],
    "GM FX Spot & Forward":         [("Sven Larsson", "FX Sales"), ("Bianca Moretti", "FX Sales")],
    "GM FX Options":                [("Sven Larsson", "FX Sales"), ("Hugo Bernard", "FX Derivatives")],
    "GM Rates Hedging":             [("Hugo Bernard", "Rates Sales")],
    "GTS Receivables Finance":      [("Elena Costa", "RF Specialist"), ("Marcus Bell", "Structured Trade")],
    "GTS Supply Chain Finance":     [("Marcus Bell", "Structured Trade"), ("Priscilla Wong", "SCF Specialist")],
    "GTS Documentary Credits":      [("Ahmed Saleh", "Trade Products")],
    "GTS Guarantees & SBLC":        [("Ahmed Saleh", "Trade Products"), ("Julia Ferreira", "Guarantees Specialist")],
    "GTS Import/Export Loans":      [("Kevin Tan", "Trade Finance")],
    "GTS Structured Trade Finance": [("Marcus Bell", "Structured Trade"), ("Elena Costa", "RF Specialist")],
    "Lending Revolving Credit":     [("Robert Frye", "Corporate Lending")],
    "Lending Term Loan":            [("Robert Frye", "Corporate Lending")],
    "Lending Asset-Based Lending":  [("Maria Santos", "ABL Specialist")],
    "IB Debt Capital Markets":      [("James Whitlock", "DCM Origination")],
    "IB M&A Advisory":              [("Charlotte Ng", "M&A Advisory")],
}

INTERNAL_TEAMS = [
    "GTS Operations", "Implementation", "Finance / Revenue Control",
    "Credit Risk", "CIB Coverage", "Supplier Engagement", "Product",
]

CASE_TYPES = [
    "Revenue recognition discrepancy",
    "Limit / utilization breach query",
    "Supplier onboarding delay",
    "Documentary discrepancy",
    "Program rollover / renewal",
    "Pricing / margin query",
    "Operational processing error",
    "Reporting / MI request",
]

# ── Client generation ──────────────────────────────────────────────────────────

def _company_name(rng, sector, intl):
    prefixes = {
        "Industrials":         ["Vanguard", "Meridian", "Atlas", "Forge", "Pinnacle"],
        "Consumer Goods":      ["Bright", "Harvest", "Nova", "Crest", "Lumen"],
        "Technology":          ["Quantum", "Cipher", "Nimbus", "Vertex", "Helix"],
        "Healthcare":          ["Vital", "Caelum", "Mercy", "Aevum", "Corpus"],
        "Energy":              ["Helios", "Volta", "Terra", "Apex", "Orbis"],
        "Automotive":          ["Axle", "Velos", "Drive", "Torque", "Caliber"],
        "Retail":              ["Marketa", "Bazaar", "Trove", "Saleem", "Vista"],
        "Chemicals":           ["Catalys", "Polymera", "Synth", "Bonded", "Ester"],
        "Aerospace & Defense": ["Aero", "Skyforge", "Falcon", "Strato", "Aegis"],
        "Metals & Mining":     ["Ferro", "Lode", "Granite", "Ore", "Smelt"],
        "Telecom":             ["Connecta", "Pulse", "Wavelength", "Nexus", "Relay"],
        "Food & Beverage":     ["Verde", "Pantry", "Brew", "Orchard", "Savor"],
        "Pharmaceuticals":     ["Curo", "Pharos", "Remedy", "Genix", "Salus"],
    }[sector]
    suf_intl = ["GmbH", "K.K.", "S.A.", "Ltd", "B.V.", "AG", "S.p.A.", "PLC"]
    suf_us   = ["Inc.", "LLC", "Corp.", "Holdings", "Group"]
    stem     = rng.choice(prefixes) + rng.choice(["", "tech", "core", "works", "lab", "tron", "ix"])
    suffix   = rng.choice(suf_intl if intl else suf_us)
    tag      = " (US)" if intl else ""
    return f"{stem.capitalize()} {suffix}{tag}"


def _build_clients():
    rng     = random.Random(SEED)
    clients = []
    for i in range(100):
        intl    = i < 49
        segment = "GNB" if (intl and rng.random() < 0.8) or (not intl and rng.random() < 0.25) else "IMM"
        sector  = rng.choice(SECTORS)
        revenue = round(rng.choice([
            rng.uniform(150, 800),
            rng.uniform(800, 4000),
            rng.uniform(4000, 18000),
        ]), 1)
        dso = rng.randint(28, 120)
        dpo = rng.randint(25, 95)
        client = {
            "id":                 f"C{i+1:03d}",
            "name":               _company_name(rng, sector, intl),
            "sector":             sector,
            "segment":            segment,
            "client_type":        "International Subsidiary" if intl else "US Domestic",
            "hq":                 rng.choice(HQ_COUNTRIES_INTL) if intl else f"{rng.choice(US_STATES)}, US",
            "revenue_usd_m":      revenue,
            "trade_volume_usd_m": round(revenue * rng.uniform(0.25, 0.75), 1),
            "dso":                dso,
            "dpo":                dpo,
            "supplier_count":     rng.randint(40, 1200),
            "trade_corridors":    rng.sample(TRADE_CORRIDORS, rng.randint(1, 4)),
            "gov_contracts":      rng.random() < 0.18,
            "relationship_years": rng.randint(1, 22),
            "enrolled":           [],
        }
        n        = rng.randint(1, 4)
        enrolled = set(rng.sample(list(PRODUCTS.keys()), n))
        if rng.random() < 0.45:
            enrolled.add(rng.choice(STRUCTURED_PRODUCTS))
        client["enrolled"] = sorted(enrolled)
        clients.append(client)
    return clients


CLIENTS = _build_clients()


# ── Program generation ─────────────────────────────────────────────────────────

def _build_programs(clients):
    rng      = random.Random(SEED + 1)
    programs = []
    pid      = 0
    for c in clients:
        for product in STRUCTURED_PRODUCTS:
            if product not in c["enrolled"]:
                continue
            pid      += 1
            is_scf    = product == "GTS Supply Chain Finance"
            limit     = round(c["trade_volume_usd_m"] * rng.uniform(0.15, 0.45), 1)
            util_pct  = rng.uniform(0.25, 1.08)
            drawn     = round(limit * util_pct, 1)
            inception = AS_OF - timedelta(days=rng.randint(120, 1100))
            tenor     = rng.choice([180, 270, 365, 540])
            rollover  = inception + timedelta(days=tenor * rng.randint(1, 4))
            while rollover < AS_OF:
                rollover += timedelta(days=tenor)
            margin_bps     = rng.randint(85, 320)
            expected_rev_k = round(drawn * 1000 * (margin_bps / 10000) / 12, 1)
            drift          = rng.uniform(-0.18, 0.06)
            booked_rev_k   = round(expected_rev_k * (1 + drift), 1)
            top_conc       = rng.uniform(0.12, 0.72)
            programs.append({
                "program_id":                f"PRG{pid:04d}",
                "client_id":                 c["id"],
                "client_name":               c["name"],
                "product":                   product,
                "type":                      "SCF" if is_scf else "RF",
                "limit_usd_m":               limit,
                "drawn_usd_m":               drawn,
                "utilization":               round(util_pct, 3),
                "inception":                 inception,
                "rollover":                  rollover,
                "days_to_rollover":          (rollover - AS_OF).days,
                "tenor_days":                tenor,
                "margin_bps":                margin_bps,
                "expected_rev_k_month":      expected_rev_k,
                "booked_rev_k_month":        booked_rev_k,
                "rev_variance_k":            round(booked_rev_k - expected_rev_k, 1),
                "rev_variance_pct":          round(drift, 3),
                "top_obligor_concentration": round(top_conc, 3),
                "dso": c["dso"],
                "dpo": c["dpo"],
            })
    return programs


PROGRAMS = _build_programs(CLIENTS)


# ── Supplier funnel ────────────────────────────────────────────────────────────

def _build_suppliers(programs):
    rng       = random.Random(SEED + 2)
    suppliers = []
    for p in programs:
        if p["type"] != "SCF":
            continue
        total        = rng.randint(12, 60)
        kyc          = int(total * rng.uniform(0.55, 0.9))
        onboarded    = int(kyc * rng.uniform(0.6, 0.95))
        discounting  = int(onboarded * rng.uniform(0.5, 0.9))
        suppliers.append({
            "program_id":            p["program_id"],
            "client_name":           p["client_name"],
            "invited":               total,
            "kyc_in_progress":       kyc,
            "onboarded":             onboarded,
            "actively_discounting":  discounting,
            "stalled":               max(0, kyc - onboarded),
        })
    return suppliers


SUPPLIERS = _build_suppliers(PROGRAMS)


# ── Cases ─────────────────────────────────────────────────────────────────────

def _build_cases(programs):
    rng   = random.Random(SEED + 3)
    cases = []
    cid   = 0
    for p in programs:
        trouble = (p["utilization"] > 1.0) or (p["rev_variance_pct"] < -0.1) \
                  or (p["days_to_rollover"] < 30) or (p["top_obligor_concentration"] > 0.6)
        n       = rng.randint(1, 2) if trouble else (1 if rng.random() < 0.25 else 0)
        for _ in range(n):
            cid    += 1
            opened  = AS_OF - timedelta(days=rng.randint(0, 45))
            status  = rng.choices(["Open", "In Progress", "Resolved"], weights=[0.35, 0.4, 0.25])[0]
            prio    = rng.choices(["High", "Medium", "Low"], weights=[0.3, 0.45, 0.25])[0]
            cases.append({
                "case_id":     f"CASE{cid:04d}",
                "program_id":  p["program_id"],
                "client_name": p["client_name"],
                "type":        rng.choice(CASE_TYPES),
                "owner_team":  rng.choice(INTERNAL_TEAMS),
                "status":      status,
                "priority":    prio,
                "opened":      opened,
                "age_days":    (AS_OF - opened).days,
                "sla_days":    rng.choice([3, 5, 10, 15]),
            })
    return cases


CASES = _build_cases(PROGRAMS)


# ── Lookups ────────────────────────────────────────────────────────────────────

def get_client(client_id):
    return next((c for c in CLIENTS if c["id"] == client_id), None)


def get_programs_for_client(client_id):
    return [p for p in PROGRAMS if p["client_id"] == client_id]


def get_cases_for_program(program_id):
    return [c for c in CASES if c["program_id"] == program_id]


def get_suppliers_for_program(program_id):
    return next((s for s in SUPPLIERS if s["program_id"] == program_id), None)


def get_bankers_for_opportunity(client, product):
    rms         = RELATIONSHIP_MANAGERS.get(client["sector"], [("Unassigned", "RM")])
    rng         = random.Random(hash(client["id"]) & 0xFFFF)
    rm          = rng.choice(rms)
    specialists = PRODUCT_SPECIALISTS.get(product, [("Unassigned", "Specialist")])
    return {"rm": rm, "specialists": specialists}
