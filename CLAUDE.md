# GTS Structured Trade Program Cockpit

Portfolio demo for the **Sales Program Manager, Global Trade Solutions** role at HSBC
(New York, GNB & IMM). Built to mirror the actual job: proactively managing live
Receivables Finance and Supply Chain Finance programs, mobilising internal
stakeholders, assuring revenue, and surfacing cross-sell expansion.

## Why it's shaped this way (read before changing anything)

The job posting is a **program-management / farmer** role, not a lead-generation
hunter role. Its verbs: *"proactively manage structured trade finance programs,"
"take ownership of client identified issues and mobilise internal stakeholders,"
"ensure balances, revenues and margins are correctly captured."* Cross-sell is
secondary ("identify opportunities for expansion of existing programs").

The app leads with a **Program Cockpit** (the day-job) and keeps cross-sell as
one tab. The program framing is the single biggest "this person gets the job"
signal in the build. Don't swap tab order without re-reading the posting first.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py

# Optional: enables live AI call brief
export ANTHROPIC_API_KEY=sk-ant-...
```

Deploy: Streamlit Community Cloud, GitHub-connected. Put the key in
`.streamlit/secrets.toml` as `ANTHROPIC_API_KEY="..."` — never commit it.

## File map

| File | Role |
|------|------|
| `app.py` | 4-tab UI. Tab order is deliberate: Cockpit → Pipeline → Deep Dive → Overview. |
| `data.py` | All mock data. `random.seed(42)`. Clients + programs, suppliers, cases. `AS_OF` is the single "today". |
| `engine.py` | Three-layer scoring: explainable waterfalls, lookalike propensity, EV ranking. Plus `program_health()`. |
| `ai_brief.py` | AI call brief. `build_brief_prompt()` always works; `generate_brief()` calls Anthropic, falls back to a template. |
| `.streamlit/config.toml` | Dark base theme. |

## The three scoring layers (each is a talking point in an interview)

1. **Explainable waterfall** — every score is `sum(named components)`, rendered as a
   Plotly waterfall. You can defend any number on screen.
2. **Lookalike propensity** — `P(product | sector, revenue band, DSO band)` computed
   from adoption in the book, Laplace-smoothed. Swap the book for real adoption data
   and the same code gives real propensity. That is the calibration story.
3. **Expected value** — `EV = propensity × revenue`, pipeline ranked by EV not raw
   score. Plus `ev_per_effort` for a "where do I spend Tuesday" efficiency view.

## Program health flags (`engine.program_health`)

Drives Tab 1. Flags: utilization breach (>100%) / near-limit (>90%), rollover
imminent (<30d) / approaching (<60d), revenue leakage (booked <-10% vs expected) /
drift (<-3%), concentration risk (top obligor >60%).
Verdict = Action Required (any red) / Watch (any amber) / Healthy.

## Good next iterations

- [ ] **Drill-through**: clicking "Open" on Tab 1 sets `focus_client`; auto-activate
      Tab 3 (needs `st.switch_page` or multipage refactor).
- [ ] **Supplier funnel on Tab 1**: per-program SCF funnel chart (data exists in `data.SUPPLIERS`).
- [ ] **Exportable call brief**: "Download brief (PDF)" button on Tab 3.
- [ ] **Scenario toggle**: "What if Fed cuts 50bps" — reprice margins, re-rank EV.
- [ ] **Wallet sizing** per client (posting mentions "wallet sizing activities").

## Guardrails

All data is synthetic (`seed=42`), pricing/margins are illustrative heuristics, and
there is no real HSBC data anywhere. Keep it that way — it is a portfolio demo.
