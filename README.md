# GTS Cross-Sell Intelligence Engine

A portfolio demo app built to illustrate a realistic workflow for the **HSBC Sales Program Manager, Global Trade Solutions** role.

**Live demo:** *(deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) for a shareable link)*

---

## What it does

Trade finance relationship managers face a classic hard problem: a portfolio of 10–50 corporate clients, each with a different mix of GTS products, different working capital profiles, and different trade corridors. The question is — **where do you focus first?**

This app simulates that workflow:

1. **Portfolio Overview** — heatmap of product penetration across the LatAm book, scatter plot of DSO vs DPO positioning, and revenue potential summary
2. **Opportunity Pipeline** — all cross-sell opportunities ranked by a multi-factor score, filtered by product and priority, with estimated annual revenue uplift
3. **Client Deep Dive** — select any client to see a radar chart of their opportunity profile and a pre-built "call brief" with specific talking points for the next relationship conversation

## Scoring logic

Each of the 6 GTS products (Supply Chain Finance, Receivables Purchase, Documentary Credits, Trade Loans, FX Hedging, Bank Guarantees) has a dedicated scorer that reads:

- Working capital metrics: DSO, DPO, trade volume
- Client profile: sector, geographies, supplier count, government contracts
- Existing product enrollment (already enrolled = deprioritized)

Scores run 0–100 and map to **High / Medium / Low** priority tiers.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (free public link)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo, set `app.py` as the entry point
4. Your shareable URL is ready in ~2 minutes
