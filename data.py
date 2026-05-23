"""Mock client portfolio — 100 US-based and international subsidiary clients."""

import random
import pandas as pd

random.seed(42)

# ── Banker rosters ─────────────────────────────────────────────────────────────
# Relationship Managers by sector coverage
RELATIONSHIP_MANAGERS = {
    "Food & Beverage":    [("Sarah Chen", "MD, CIB Coverage"), ("Michael Torres", "Director, CIB Coverage"), ("Priya Nair", "VP, CIB Coverage")],
    "Agriculture":        [("James Whitfield", "MD, Agribusiness Coverage"), ("Laura Simmons", "Director, CIB Coverage")],
    "Technology":         [("David Park", "MD, TMT Coverage"), ("Nina Patel", "Director, TMT Coverage"), ("Ryan Okafor", "VP, TMT Coverage")],
    "Pharmaceuticals":    [("Catherine Lowe", "MD, Healthcare Coverage"), ("Marcus Webb", "Director, Healthcare Coverage")],
    "Energy":             [("Robert Haines", "MD, Energy Coverage"), ("Alicia Moreno", "Director, Energy Coverage"), ("Tom Lindqvist", "VP, Natural Resources")],
    "Chemicals":          [("George Stafford", "MD, Industrials Coverage"), ("Angela Kim", "Director, Chemicals Coverage")],
    "Manufacturing":      [("Philip Osei", "MD, Industrials Coverage"), ("Hannah Bryce", "Director, Manufacturing Coverage"), ("Stefan Nowak", "VP, Industrials Coverage")],
    "Retail":             [("Jessica Flynn", "MD, Consumer Coverage"), ("Carlos Espinoza", "Director, Consumer Coverage")],
    "Construction":       [("Andrew MacPherson", "MD, Infrastructure Coverage"), ("Mei Lin", "Director, Construction Coverage")],
    "Apparel":            [("Olivia Grant", "MD, Consumer Coverage"), ("Kevin Chandra", "Director, Retail Coverage")],
    "Mining":             [("Samuel Obi", "MD, Natural Resources Coverage"), ("Rachel Thorpe", "Director, Mining Coverage")],
    "Infrastructure":     [("Brian Kowalski", "MD, Infrastructure Coverage"), ("Fatima Al-Rashid", "Director, Infrastructure Coverage")],
    "Financial Services": [("William Hargreaves", "MD, FIG Coverage"), ("Diane Cho", "Director, FIG Coverage")],
}

# Product Specialists by product line
PRODUCT_SPECIALISTS = {
    "GPS - Current Accounts":       [("Jonathan Reeves", "MD, GPS Sales"), ("Amara Diallo", "Director, Transaction Banking Sales")],
    "GPS - Savings & Deposits":     [("Jonathan Reeves", "MD, GPS Sales"), ("Sophie Eriksson", "VP, Deposits & Liquidity Sales")],
    "GPS - Term Deposits":          [("Sophie Eriksson", "VP, Deposits & Liquidity Sales"), ("Jonathan Reeves", "MD, GPS Sales")],
    "GPS - Liquidity & Channel":    [("Maya Goldstein", "MD, Liquidity Solutions"), ("Jonathan Reeves", "MD, GPS Sales")],
    "GPS - International Payments": [("Diego Ramirez", "MD, Payments Sales"), ("Amara Diallo", "Director, Transaction Banking Sales")],
    "GPS - Domestic Payments":      [("Diego Ramirez", "MD, Payments Sales"), ("Lena Hoffmann", "VP, Payments Solutions")],
    "GPS - Cards":                  [("Fiona MacLeod", "Director, Commercial Cards"), ("Diego Ramirez", "MD, Payments Sales")],
    "GM - Forex - Cash":            [("Alexander Novak", "MD, FX Sales"), ("Chloe Beaumont", "Director, FX Structuring"), ("Patrick Daly", "VP, FX Sales")],
    "GM - FOREX - TFX":             [("Patrick Daly", "VP, FX Sales"), ("Alexander Novak", "MD, FX Sales")],
    "GM - Futures":                 [("Raj Krishnamurthy", "MD, Commodities & Derivatives"), ("Isabelle Fontaine", "Director, Structured Derivatives")],
    "GTS - Supply Chain Solutions": [("Trevor Blake", "MD, GTS Sales"), ("Yuki Tanaka", "Director, Supply Chain Finance"), ("Claudia Vega", "VP, GTS Sales")],
    "GTS - Receivables Finance":    [("Trevor Blake", "MD, GTS Sales"), ("Omar Hassan", "Director, Receivables Finance"), ("Claudia Vega", "VP, GTS Sales")],
    "GTS - Documentary Trade":      [("Sandra Petrov", "MD, Documentary Trade"), ("Yuki Tanaka", "Director, Supply Chain Finance")],
    "GTS - Trade Loans":            [("Trevor Blake", "MD, GTS Sales"), ("Sandra Petrov", "MD, Documentary Trade"), ("Omar Hassan", "Director, Receivables Finance")],
    "GTS - Guarantees":             [("Sandra Petrov", "MD, Documentary Trade"), ("Claudia Vega", "VP, GTS Sales")],
    "GTS - CSTF":                   [("Nathaniel Cross", "MD, Commodity-Structured Trade"), ("Raj Krishnamurthy", "MD, Commodities & Derivatives")],
    "Lending - Corporate Lending":  [("Eleanor Hayes", "MD, Corporate Lending"), ("Marcus Webb", "Director, Healthcare Coverage"), ("Philip Osei", "MD, Industrials Coverage")],
    "IB - DCM IG":                  [("Victoria Sterling", "MD, DCM"), ("Harrison Cole", "Director, Debt Capital Markets"), ("Isabelle Fontaine", "Director, Structured Derivatives")],
}

GTS_PRODUCTS = [
    "GPS - Current Accounts",
    "GPS - Savings & Deposits",
    "GPS - Term Deposits",
    "GPS - Liquidity & Channel",
    "GPS - International Payments",
    "GPS - Domestic Payments",
    "GPS - Cards",
    "GM - Forex - Cash",
    "GM - FOREX - TFX",
    "GM - Futures",
    "GTS - Supply Chain Solutions",
    "GTS - Receivables Finance",
    "GTS - Documentary Trade",
    "GTS - Trade Loans",
    "GTS - Guarantees",
    "GTS - CSTF",
    "Lending - Corporate Lending",
    "IB - DCM IG",
]

PRODUCT_CATEGORIES = {
    "GPS": [p for p in GTS_PRODUCTS if p.startswith("GPS")],
    "GM": [p for p in GTS_PRODUCTS if p.startswith("GM")],
    "GTS": [p for p in GTS_PRODUCTS if p.startswith("GTS")],
    "Lending": [p for p in GTS_PRODUCTS if p.startswith("Lending")],
    "IB": [p for p in GTS_PRODUCTS if p.startswith("IB")],
}

# ── US Domestic corporates ─────────────────────────────────────────────────────
US_CLIENTS_RAW = [
    # Food & Beverage
    ("Heartland Foods Group", "Food & Beverage", "Chicago, IL", ["USA", "Canada", "Mexico"], 1800, 820, 68, 42, 580, False, True, False),
    ("Prairie Grain Co.", "Food & Beverage", "Kansas City, MO", ["USA", "China", "Japan", "EU"], 3200, 2100, 88, 38, 720, True, False, True),
    ("Southern Beverage Corp", "Food & Beverage", "Atlanta, GA", ["USA", "Canada", "Caribbean"], 950, 410, 52, 31, 310, False, False, True),
    ("Great Lakes Dairy", "Food & Beverage", "Detroit, MI", ["USA", "Canada"], 620, 180, 44, 29, 140, False, False, True),
    ("Pacific Coast Seafood", "Food & Beverage", "Seattle, WA", ["USA", "Japan", "China", "South Korea"], 740, 590, 91, 22, 85, True, False, True),
    ("Texas Cattle Holdings", "Food & Beverage", "Dallas, TX", ["USA", "Mexico", "Japan", "South Korea"], 2400, 1380, 77, 44, 420, True, False, True),
    ("Sunshine Organics", "Food & Beverage", "San Francisco, CA", ["USA", "Canada", "EU"], 310, 140, 58, 35, 190, True, False, False),
    # Agriculture
    ("Midwest Agri Partners", "Agriculture", "Des Moines, IA", ["USA", "China", "Brazil", "EU"], 4100, 2900, 94, 47, 890, True, False, True),
    ("Delta Cotton Corp", "Agriculture", "Memphis, TN", ["USA", "China", "India", "Turkey"], 1650, 1240, 86, 39, 340, True, False, True),
    ("Mountain States Grain", "Agriculture", "Denver, CO", ["USA", "Mexico", "Japan"], 890, 620, 72, 41, 260, True, False, True),
    ("Appalachian Timber LLC", "Agriculture", "Charlotte, NC", ["USA", "China", "EU", "Canada"], 560, 410, 65, 33, 95, True, False, False),
    # Technology
    ("Silicon Valley Semiconductor", "Technology", "San Jose, CA", ["USA", "Taiwan", "South Korea", "Japan", "EU"], 6800, 3900, 78, 55, 180, True, False, True),
    ("Midwest Tech Manufacturing", "Technology", "Columbus, OH", ["USA", "China", "Mexico", "Canada"], 1200, 740, 65, 43, 210, True, False, True),
    ("Atlantic Software Systems", "Technology", "Boston, MA", ["USA", "EU", "Canada"], 980, 290, 71, 38, 95, True, False, False),
    ("CloudEdge Networks", "Technology", "Austin, TX", ["USA", "EU", "Singapore", "Canada"], 540, 180, 59, 44, 65, True, False, False),
    ("Phoenix Data Solutions", "Technology", "Phoenix, AZ", ["USA", "Canada", "Mexico"], 380, 110, 63, 48, 72, False, True, False),
    # Pharmaceuticals
    ("Northeast Pharma Group", "Pharmaceuticals", "New York, NY", ["USA", "EU", "Canada", "Japan"], 3400, 1100, 82, 68, 320, True, True, False),
    ("Appalachian BioSciences", "Pharmaceuticals", "Raleigh, NC", ["USA", "EU", "China"], 890, 310, 74, 61, 145, True, True, False),
    ("Southwest Medical Supply", "Pharmaceuticals", "Albuquerque, NM", ["USA", "Mexico", "Canada"], 420, 195, 57, 44, 230, False, True, False),
    ("Great Plains Health Corp", "Pharmaceuticals", "Omaha, NE", ["USA", "Canada"], 610, 220, 66, 52, 185, False, True, False),
    # Energy
    ("Gulf Coast Energy Partners", "Energy", "Houston, TX", ["USA", "Canada", "Mexico", "Saudi Arabia"], 8200, 4100, 55, 61, 95, True, True, False),
    ("Rocky Mountain Gas LLC", "Energy", "Denver, CO", ["USA", "Canada", "Mexico"], 3100, 1800, 48, 55, 75, True, True, False),
    ("Appalachian Power Services", "Energy", "Pittsburgh, PA", ["USA", "Canada"], 1400, 680, 62, 47, 120, False, True, False),
    ("Solar Horizon Corp", "Energy", "Phoenix, AZ", ["USA", "Germany", "China", "Japan"], 920, 510, 77, 38, 68, True, True, False),
    ("Atlantic Offshore Energy", "Energy", "Norfolk, VA", ["USA", "EU", "Canada"], 1750, 890, 58, 54, 88, True, True, False),
    # Chemicals
    ("Great Lakes Chemical Co.", "Chemicals", "Cleveland, OH", ["USA", "Canada", "EU", "China"], 2100, 1340, 71, 58, 230, True, False, False),
    ("Gulf Petrochem Corp", "Chemicals", "Baton Rouge, LA", ["USA", "Mexico", "Brazil", "EU"], 3600, 2200, 64, 62, 175, True, False, False),
    ("Southwest Specialty Chem", "Chemicals", "Houston, TX", ["USA", "Mexico", "Canada"], 780, 490, 68, 51, 140, True, False, False),
    ("Appalachian Industrial Chem", "Chemicals", "Charleston, WV", ["USA", "Canada", "EU"], 560, 370, 73, 49, 120, False, False, False),
    # Manufacturing
    ("Great Plains Auto Parts", "Manufacturing", "Detroit, MI", ["USA", "Mexico", "Canada", "China"], 2800, 1650, 69, 57, 480, True, False, True),
    ("Southeast Aerospace Group", "Manufacturing", "Huntsville, AL", ["USA", "EU", "Canada"], 4200, 1900, 83, 72, 320, True, True, False),
    ("Midwest Steel & Fabrication", "Manufacturing", "Gary, IN", ["USA", "Canada", "Mexico", "Brazil"], 1350, 920, 74, 63, 290, True, False, False),
    ("Pacific Northwest Lumber", "Manufacturing", "Portland, OR", ["USA", "China", "Japan", "Canada"], 680, 540, 61, 35, 95, True, False, True),
    ("Texas Industrial Machinery", "Manufacturing", "San Antonio, TX", ["USA", "Mexico", "Brazil", "Canada"], 1100, 730, 77, 54, 210, True, False, False),
    ("Atlantic Shipbuilding Corp", "Manufacturing", "Baltimore, MD", ["USA", "EU", "Middle East"], 2100, 980, 91, 68, 185, True, True, False),
    ("Rocky Mountain Mining Equipment", "Manufacturing", "Salt Lake City, UT", ["USA", "Canada", "Australia", "Chile"], 890, 620, 79, 55, 155, True, True, False),
    # Retail
    ("Mid-Atlantic Retail Group", "Retail", "Philadelphia, PA", ["USA", "Canada", "China"], 2200, 1400, 48, 31, 920, False, False, True),
    ("Sunbelt Consumer Goods", "Retail", "Miami, FL", ["USA", "Latin America", "Canada"], 1650, 980, 52, 28, 740, False, False, True),
    ("Pacific Rim Trading Co.", "Retail", "Los Angeles, CA", ["USA", "China", "Japan", "South Korea"], 3100, 2100, 57, 34, 1100, False, False, True),
    ("Mountain West Wholesale", "Retail", "Las Vegas, NV", ["USA", "Canada", "Mexico"], 780, 510, 44, 26, 560, False, False, True),
    # Construction & Infrastructure
    ("Northeast Infrastructure Group", "Construction", "New York, NY", ["USA", "Canada", "EU"], 1900, 680, 102, 61, 420, False, True, False),
    ("Gulf Coast Contractors", "Construction", "New Orleans, LA", ["USA", "Mexico", "Caribbean"], 820, 310, 95, 54, 310, False, True, False),
    ("Southwest Civil Engineering", "Construction", "Las Vegas, NV", ["USA", "Mexico", "Canada"], 610, 240, 88, 57, 270, False, True, False),
    ("Pacific Infrastructure Partners", "Construction", "Los Angeles, CA", ["USA", "Canada", "Japan"], 1400, 490, 97, 63, 350, False, True, False),
    # Apparel & Textiles
    ("New York Fashion Group", "Apparel", "New York, NY", ["USA", "China", "Bangladesh", "EU", "Vietnam"], 1100, 830, 79, 38, 680, True, False, True),
    ("Southeast Textile Mills", "Apparel", "Greenville, SC", ["USA", "China", "India", "EU"], 490, 370, 71, 42, 420, True, False, True),
    ("West Coast Sportswear", "Apparel", "Los Angeles, CA", ["USA", "China", "Vietnam", "Indonesia", "EU"], 870, 650, 74, 35, 780, True, False, True),
    # Mining & Metals
    ("Arizona Copper Mining", "Mining", "Tucson, AZ", ["USA", "China", "Japan", "EU"], 2100, 1650, 62, 58, 95, True, True, False),
    ("Nevada Gold Corp", "Mining", "Reno, NV", ["USA", "EU", "Canada", "Australia"], 1800, 1240, 55, 61, 78, True, True, False),
    ("Appalachian Coal Holdings", "Mining", "Lexington, KY", ["USA", "India", "EU", "Japan"], 940, 720, 68, 49, 62, True, True, False),
    ("Great Plains Ethanol Corp", "Energy", "Sioux Falls, SD", ["USA", "Canada", "Brazil", "EU"], 580, 390, 61, 43, 75, True, False, True),
]

# ── International Subsidiary clients in the US ────────────────────────────────
INTL_CLIENTS_RAW = [
    # German
    ("Müller Automotive USA", "Manufacturing", "Detroit, MI", ["USA", "Germany", "Mexico", "China"], 3800, 2100, 61, 72, 420, True, False, True),
    ("Bayer Healthcare Americas", "Pharmaceuticals", "Whippany, NJ", ["USA", "Germany", "EU", "Japan", "China"], 4200, 1300, 85, 78, 285, True, True, False),
    ("BASF North America Corp", "Chemicals", "Florham Park, NJ", ["USA", "Germany", "Canada", "Mexico", "EU"], 5100, 2900, 69, 74, 310, True, False, False),
    ("Siemens Energy Americas", "Energy", "Houston, TX", ["USA", "Germany", "EU", "Middle East"], 3600, 1700, 72, 68, 195, True, True, False),
    ("Bosch Manufacturing USA", "Manufacturing", "Anderson, SC", ["USA", "Germany", "Mexico", "China", "India"], 2900, 1650, 65, 71, 380, True, False, True),
    ("ThyssenKrupp Steel Americas", "Manufacturing", "Calvert, AL", ["USA", "Germany", "Brazil", "Canada"], 1800, 1380, 74, 69, 215, True, False, False),
    ("Henkel Consumer Americas", "Chemicals", "Stamford, CT", ["USA", "Germany", "Canada", "Mexico", "EU"], 2100, 980, 66, 63, 240, True, False, True),
    # Japanese
    ("Toyota Motor North America", "Manufacturing", "Plano, TX", ["USA", "Japan", "Mexico", "Canada", "EU"], 18000, 8400, 58, 81, 640, True, False, True),
    ("Sony Electronics Americas", "Technology", "San Diego, CA", ["USA", "Japan", "Mexico", "EU", "China"], 4800, 2200, 71, 68, 185, True, False, True),
    ("Mitsubishi Chemical Americas", "Chemicals", "Alpharetta, GA", ["USA", "Japan", "EU", "China"], 2600, 1540, 68, 72, 195, True, False, False),
    ("Sumitomo Corp of Americas", "Manufacturing", "New York, NY", ["USA", "Japan", "EU", "China", "Southeast Asia"], 6200, 3800, 75, 65, 310, True, False, False),
    ("Hitachi Energy Americas", "Energy", "Raleigh, NC", ["USA", "Japan", "EU", "Canada"], 3100, 1450, 79, 63, 165, True, True, False),
    ("Canon USA Inc", "Technology", "Melville, NY", ["USA", "Japan", "EU", "China"], 2400, 1100, 64, 61, 140, True, False, True),
    ("Bridgestone Americas", "Manufacturing", "Nashville, TN", ["USA", "Japan", "Mexico", "Canada", "Brazil"], 4900, 2400, 62, 74, 380, True, False, True),
    # British
    ("BP North America Inc", "Energy", "Houston, TX", ["USA", "UK", "Canada", "Middle East", "Norway"], 22000, 11000, 44, 58, 88, True, True, False),
    ("Rolls-Royce Americas", "Manufacturing", "Reston, VA", ["USA", "UK", "EU", "Canada"], 5800, 2100, 88, 75, 145, True, True, False),
    ("AstraZeneca US Operations", "Pharmaceuticals", "Wilmington, DE", ["USA", "UK", "EU", "Japan", "China"], 7400, 2100, 91, 82, 220, True, True, False),
    ("HSBC Global Banking Americas", "Financial Services", "New York, NY", ["USA", "UK", "EU", "Asia", "Latin America"], 0, 0, 0, 0, 0, True, False, False),
    ("BAE Systems Inc", "Manufacturing", "Arlington, VA", ["USA", "UK", "EU", "Australia"], 6200, 2800, 94, 71, 195, True, True, False),
    ("Diageo North America", "Food & Beverage", "Norwalk, CT", ["USA", "UK", "EU", "Caribbean", "Canada"], 3800, 1200, 57, 48, 280, True, False, True),
    # French
    ("Total Energies USA", "Energy", "Houston, TX", ["USA", "France", "EU", "Middle East", "Africa"], 14000, 7800, 47, 62, 95, True, True, False),
    ("Airbus Americas Inc", "Manufacturing", "Mobile, AL", ["USA", "France", "EU", "Canada"], 8900, 3100, 96, 84, 165, True, True, False),
    ("L'Oréal USA Inc", "Retail", "New York, NY", ["USA", "France", "EU", "China", "Canada"], 4200, 1350, 61, 52, 380, True, False, True),
    ("Michelin North America", "Manufacturing", "Greenville, SC", ["USA", "France", "EU", "Canada", "Brazil"], 3600, 1900, 65, 69, 310, True, False, True),
    ("Schneider Electric USA", "Manufacturing", "Boston, MA", ["USA", "France", "EU", "Mexico", "Canada"], 4800, 2200, 72, 67, 245, True, False, False),
    # South Korean
    ("Samsung Electronics America", "Technology", "Ridgefield Park, NJ", ["USA", "South Korea", "EU", "China", "Vietnam"], 9800, 4200, 74, 65, 210, True, False, True),
    ("Hyundai Motor America", "Manufacturing", "Fountain Valley, CA", ["USA", "South Korea", "Mexico", "EU"], 12000, 5800, 62, 77, 420, True, False, True),
    ("LG Electronics USA", "Technology", "Englewood Cliffs, NJ", ["USA", "South Korea", "EU", "China", "Mexico"], 5200, 2400, 68, 63, 185, True, False, True),
    ("SK Innovation Americas", "Energy", "Atlanta, GA", ["USA", "South Korea", "EU", "China"], 3400, 1800, 71, 68, 145, True, False, False),
    ("POSCO Americas Corp", "Manufacturing", "Songdo, GA", ["USA", "South Korea", "EU", "Australia", "Brazil"], 2800, 1950, 66, 72, 165, True, False, False),
    # Chinese
    ("Lenovo North America", "Technology", "Morrisville, NC", ["USA", "China", "EU", "Canada", "Latin America"], 6800, 3100, 77, 58, 175, True, False, True),
    ("CNOOC USA Inc", "Energy", "Houston, TX", ["USA", "China", "Canada", "Australia"], 4200, 2800, 51, 61, 72, True, True, False),
    ("Haier Americas", "Manufacturing", "Camden, SC", ["USA", "China", "EU", "Canada"], 2100, 980, 69, 54, 215, True, False, True),
    # Canadian
    ("Brookfield Asset Mgmt USA", "Infrastructure", "New York, NY", ["USA", "Canada", "EU", "Australia"], 8400, 2100, 88, 74, 135, False, True, False),
    ("Bombardier Transportation", "Manufacturing", "Plattsburgh, NY", ["USA", "Canada", "EU", "Middle East"], 3200, 1450, 94, 79, 125, True, True, False),
    ("Manulife US Operations", "Financial Services", "Boston, MA", ["USA", "Canada", "EU", "Asia"], 0, 0, 0, 0, 0, False, False, False),
    # Dutch / Swiss
    ("Shell USA Inc", "Energy", "Houston, TX", ["USA", "Netherlands", "EU", "Canada", "Middle East"], 19000, 9800, 43, 65, 92, True, True, False),
    ("Philips North America", "Technology", "Andover, MA", ["USA", "Netherlands", "EU", "China", "Canada"], 3800, 1600, 73, 68, 185, True, False, False),
    ("Nestlé USA Inc", "Food & Beverage", "Arlington, VA", ["USA", "Switzerland", "EU", "Canada", "Mexico"], 7200, 2100, 55, 49, 610, True, False, True),
    ("Novartis Pharmaceuticals USA", "Pharmaceuticals", "East Hanover, NJ", ["USA", "Switzerland", "EU", "Japan", "China"], 8900, 2400, 88, 81, 275, True, True, False),
    ("ABB Group North America", "Manufacturing", "Cary, NC", ["USA", "Switzerland", "EU", "Canada", "China"], 4100, 1850, 77, 71, 210, True, False, False),
    ("Roche Diagnostics Corp", "Pharmaceuticals", "Indianapolis, IN", ["USA", "Switzerland", "EU", "Japan", "Canada"], 6200, 1800, 84, 77, 240, True, True, False),
    # Indian
    ("Tata Consultancy US", "Technology", "Edison, NJ", ["USA", "India", "EU", "Canada", "Australia"], 4800, 980, 82, 61, 165, True, False, False),
    ("Infosys Americas", "Technology", "Raleigh, NC", ["USA", "India", "EU", "Canada", "Australia"], 3900, 740, 79, 57, 145, True, False, False),
    ("Wipro Americas Inc", "Technology", "San Jose, CA", ["USA", "India", "EU", "Canada", "Middle East"], 2800, 510, 74, 53, 120, True, False, False),
    # Swedish / Nordic
    ("Volvo North America", "Manufacturing", "Greensboro, NC", ["USA", "Sweden", "EU", "Canada", "Mexico"], 5100, 2600, 71, 75, 285, True, False, True),
    ("IKEA North America Services", "Retail", "Conshohocken, PA", ["USA", "Sweden", "EU", "China", "Canada"], 4400, 2100, 49, 62, 840, False, False, True),
    ("Ericsson Inc (USA)", "Technology", "Plano, TX", ["USA", "Sweden", "EU", "Latin America", "Asia"], 3200, 1100, 77, 65, 150, True, False, False),
    ("H&M Hennes & Mauritz USA", "Apparel", "New York, NY", ["USA", "Sweden", "EU", "China", "Bangladesh", "Vietnam"], 2800, 1950, 56, 41, 920, True, False, True),
    ("Equinor US Operations", "Energy", "Stamford, CT", ["USA", "Norway", "EU", "Canada"], 9200, 5400, 46, 59, 85, True, True, False),
    ("ABB Asea Brown Boveri", "Manufacturing", "Cary, NC", ["USA", "Switzerland", "EU", "China", "India"], 3200, 1450, 74, 68, 195, True, False, False),
]

# Remove HSBC and financial services clients with zero trade (not applicable for GTS)
INTL_CLIENTS_RAW = [c for c in INTL_CLIENTS_RAW if c[4] > 0]


def _build_client(row, is_intl: bool) -> dict:
    name, sector, hq, geos, rev, trade, dso, dpo, suppliers, fx, govt, seasonal = row
    n_products = random.randint(1, 4)
    eligible = [p for p in GTS_PRODUCTS]
    current = random.sample(eligible, min(n_products, len(eligible)))
    rm_pool = RELATIONSHIP_MANAGERS.get(sector, [("Alex Johnson", "MD, CIB Coverage")])
    rm = rm_pool[random.randint(0, len(rm_pool) - 1)]
    return {
        "client": name,
        "sector": sector,
        "hq": hq,
        "trade_geographies": geos,
        "annual_revenue_usd_m": rev,
        "trade_volume_usd_m": trade,
        "dso_days": dso,
        "dpo_days": dpo,
        "supplier_count": suppliers,
        "multi_currency": fx,
        "government_contracts": govt,
        "seasonal_trade": seasonal,
        "current_products": current,
        "relationship_years": random.randint(1, 12),
        "client_type": "International Subsidiary" if is_intl else "US Domestic",
        "relationship_manager": rm[0],
        "rm_title": rm[1],
    }


def get_bankers_for_opportunity(client: dict, product: str) -> dict:
    """Return RM and product specialist(s) for a given client + product."""
    rm_pool = RELATIONSHIP_MANAGERS.get(client["sector"], [("Alex Johnson", "MD, CIB Coverage")])
    rm = (client["relationship_manager"], client["rm_title"])
    specialists = PRODUCT_SPECIALISTS.get(product, [("Trevor Blake", "MD, GTS Sales")])
    return {"rm": rm, "specialists": specialists}


CLIENTS = (
    [_build_client(r, False) for r in US_CLIENTS_RAW]
    + [_build_client(r, True) for r in INTL_CLIENTS_RAW]
)


def get_portfolio_df() -> pd.DataFrame:
    rows = []
    for c in CLIENTS:
        rows.append({
            "Client": c["client"],
            "Type": c["client_type"],
            "Sector": c["sector"],
            "HQ": c["hq"],
            "Revenue ($M)": c["annual_revenue_usd_m"],
            "Trade Volume ($M)": c["trade_volume_usd_m"],
            "DSO (days)": c["dso_days"],
            "DPO (days)": c["dpo_days"],
            "Suppliers": c["supplier_count"],
            "Geographies": len(c["trade_geographies"]),
            "Current Products": len(c["current_products"]),
            "Relationship (yrs)": c["relationship_years"],
        })
    return pd.DataFrame(rows)
