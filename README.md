# US Flight Operations — A Plain-English Look at 2015 Delays

**Data Visualization & Analytics (DVA) · Capstone 2 · Final project**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas)](https://pandas.pydata.org/)
[![Tableau](https://img.shields.io/badge/Visuals-Tableau-E97627?logo=tableau)](https://public.tableau.com/)

| Item | Detail |
|:-----|:---------|
| **Sector** | Aviation / transportation |
| **Team** | Section D — Group 19 |
| **Institute** | Newton School of Technology |
| **Program** | Data Visualization & Analytics — Capstone 2 |
| **Year of data** | 2015 (US domestic) |
| **Repository** | [github.com/adamyatiwari12/SectionD_G19_FlightOps-Dashboard](https://github.com/adamyatiwari12/SectionD_G19_FlightOps-Dashboard) |

We analyzed a **stratified sample of 100,000 flights** from official 2015 on-time data to see **when** delays happen, **why** they happen, and what airlines and airports could change. **Python** (pandas, NumPy, SciPy/statsmodels) drives cleaning and statistics; **Tableau Public** hosts four interactive dashboards. The long-form write-up, tables, and contribution matrix are in **[`reports/project_report.pdf`](reports/project_report.pdf)**.

---

## Why this matters

US commercial aviation moves hundreds of millions of passengers each year. Delays cascade: one late departure rolls into the next leg, crews and gates slip, and connections break. Industry and FAA context treat delay minutes as expensive once fuel, crew, compensation, and rebooking are included — so **small operational fixes at the right hubs and times** can matter at network scale. Our work is descriptive (2015, historic sample), not a live prediction product — but it is **reproducible**, **statistically checked**, and **decision-oriented**.

**Who can use the results:** airline ops (buffers, turnaround), airport ops (ground/taxi bottlenecks), and policy readers (cancellation-rate heterogeneity).

---

## The question

> Using 2015 US flight data, **which airlines, airports, times, and delay drivers** explain the most delay — and **what should be fixed first?**

**In scope:** domestic 2015 operations; delays by carrier, airport, route, time of day, and season; cancellations and stated delay causes.  
**Out of scope:** international and cargo, real-time prediction, pricing / loyalty / revenue.

**Success criteria (how we judged the project):** reproducible pipeline, statistical support for major claims, multi-view Tableau with filters, recommendations tied to measured effects, public GitHub.

---

## By the numbers (100K-flight sample)

| Metric | Value | Note |
|--------|------:|------|
| Flights | **100,000** | Stratified from full 2015 OTP population |
| **On-time rate** | **81.8%** | Arrival within 15 minutes of schedule |
| **Average arrival delay** | **4.4 min** | Mean; long tail of severe delays |
| **Cancelled** | **1.55%** | Roughly 1 in 65 flights |

---

## Four main findings

1. **Departure and arrival delay move together** (Pearson **r ≈ 0.94**). Fixing late departures addresses most of the arrival-delay problem in a linear sense — the “cascade” shows up clearly in the data.
2. **Late aircraft / cascade and airline–system causes dominate delay minutes** in the breakdown you’ll see in the dashboard; weather shows up more in **cancellations** than in routine delay minutes.
3. **Airlines differ a lot in average arrival delay** (best vs worst on the order of **~14 minutes** in this sample — statistically distinct via ANOVA and follow-ups; see report).
4. **Time of day dominates** average delay: **mornings are smoother**; **evening** blocks show much higher average arrival delay than morning for comparable traffic.

---

## Top recommendations (summary)

Full text, assumptions, and dollar logic are in **§10–11** of the report.

1. **Departure discipline at the busiest hubs** — reduce gate/pushback slippage where cascade risk is highest.  
2. **Bias important and connecting flights toward morning banks** where the data show lower average delay.  
3. **Turnaround and ground-process focus at chronically stressed hubs** (report highlights ORD, EWR, SFO patterns in rankings).  
4. **Seasonal capacity** — pre-position crew/standby for **summer** and **winter holiday** peaks (recurring in monthly views).  
5. **Regulatory / fairness lens** on carriers with unusually high cancellation rates relative to peers (chi-squared link airline ↔ cancellation mix).

Impact discussion in the report uses the **~$74/minute** benchmark for delay cost (2015-era sources, cited there) and scales **sample → full-year** with explicit caveats — **estimates, not guarantees**.

---

## Data source & files

| Asset | Rows | Role |
|--------|-----:|------|
| **BTS 2015 On-Time Performance** | 5.83M (full) | Official US DOT domestic flight records |
| **Sample `flights`** | **100,000** | Stratified for laptop-friendly notebooks; preserves month/airline/airport mix |
| **`airlines.csv`** | 14 | Carrier codes and names |
| **`airports.csv`** | 322 | Airports and locations |

Important fields (plain English): **`AIRLINE`**, **`ORIGIN_AIRPORT` / `DESTINATION`**, **`DEPARTURE_DELAY`**, **`ARRIVAL_DELAY`**, taxi times, **distance**, **cancellation**, **diversion**, five **delay-cause** columns, **`CANCELLATION_REASON`**.

**Limitations:** single year (2015); cause codes are carrier-reported; a slice of rows has legacy airport codes (location gaps); sample can under-represent very rare events.

Full column dictionary: [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## Cleaning & ETL (high level)

Executed in **Jupyter** + **`scripts/etl_pipeline.py`**. Examples of steps:

- Missing delay-cause cells treated as **0** (no delay of that type).  
- Missing cancellation reason → **“Not Cancelled”**.  
- Built **`DATE`**, **`TIME_OF_DAY`**, **`DELAY_CATEGORY`**, **`PRIMARY_DELAY_CAUSE`**, **`ROUTE`**, joins for **airline/airport names** and geo.  
- **Category dtypes** to reduce memory; kept **extreme delays** as real outcomes, not arbitrary drops.

Detailed step-by-step table → **report §4**.

---

## KPI framework

| KPI | Idea | Why it matters |
|-----|------|----------------|
| **On-time rate** | Share arrivals ≤ 15 min | Headline reliability |
| **Average arrival delay** | Mean minutes late | Compare carriers / months |
| **Cancellation rate** | % cancelled | Schedule integrity |
| **Severity mix** | Early vs minor vs severe | Tail risk beyond the mean |
| **Cascade strength** | Dep ↔ arr relationship | Where to intervene first |
| **Main delay reason** | Dominant stated cause | Budget and ops focus |

Notebook **`05_final_load_prep.ipynb`** prepares **seven Tableau-ready CSVs** (see [`tableau/dashboard_links.md`](tableau/dashboard_links.md) for the map).

---

## Statistical validation (snapshot)

| Claim | Approach | Report takeaway |
|-------|----------|-----------------|
| Airlines differ on delay | **ANOVA** | Large **F**, **p ≈ 0** |
| Cancellation mix ↔ carrier | **Chi-squared** | Strong association |
| Departure ↔ arrival | **Pearson r** | **r ≈ 0.94** |
| Predict arrival delay | **Multiple regression** | Very high **R²** (~0.94; see report — overfitting caveats apply) |
| Time-of-day effect | **Kruskal–Wallis** | Significant |

Seven tests and interpretation → **report §7**. *P*-values reported there are tiny vs 0.05; read **§12** for what statistics *cannot* prove (causality, passenger-level connections, etc.).

---

## Tableau dashboards (four views)

Live URLs and file lineage → **[`tableau/dashboard_links.md`](tableau/dashboard_links.md)**. Screenshots → **`tableau/screenshots/`** (add images if not yet committed).

| # | Focus | Answers |
|---|--------|---------|
| **1** | Operations overview | Volume, on-time %, mean delay, cancellations, monthly & weekday patterns |
| **2** | Delay analysis | Dep–arr cascade, time-of-day curve, cause mix, airline comparisons |
| **3** | Routes & airports | Map, busy routes, airport delay rankings |
| **4** | Airline comparison | On-time and delay scorecards, cancellation heatmaps, share |

Each workbook includes **interactive filters** (month, airline, time bucket, etc.).

---

## Twelve insights (headlines)

One-line versions; full “decision language” in **report §9**.

1. Fix departures → you address most arrival delay (cascade).  
2. Mornings beat evenings for average delay.  
3. Thu/Fri tend to be rougher than Sat; patterns tie to network stress, not only volume.  
4. Late-aircraft + airline-side causes dominate many delay narratives vs weather-as-delay.  
5. Alaska / Hawaiian punch above average on punctuality in this sample.  
6. ORD / EWR / SFO recur in “pain” lists; **ATL** shows high volume with moderate delay.  
7. Weather vs airline issues split **cancellations** vs **delay minutes** differently.  
8. Distance buckets don’t explain delay the way ground/turnaround story does.  
9. Severe tail (<1% of flights **>3h** late) drives much of passenger pain.  
10. Seasonality: summer + winter holiday peaks repeat.  
11. Delays are **systematic**, not iid noise (strong modeled fit — interpret carefully).  
12. Best vs worst carrier gap is operationally large even when some effect sizes look “medium” in Cohen’s *d*.

---

## Pipeline & repository layout

```mermaid
graph LR
    A[BTS raw / sample] --> B[Notebooks + etl_pipeline.py]
    B --> C[data/processed]
    C --> D[Stats + KPIs]
    D --> E[tableau/*.csv]
    E --> F[Tableau Public]
```

```text
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb           # Core ETL + exploratory views
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
├── scripts/
│   ├── etl_pipeline.py
│   ├── sample_dataset.py           # e.g. 5.8M → 100K stratified
│   └── tableau_prep.py
├── data/raw/   data/processed/   data/processed/tableau/
├── docs/data_dictionary.md
├── tableau/dashboard_links.md    tableau/screenshots/
├── reports/project_report.pdf    reports/presentation.pdf
├── dva-oriented-resume/          dva-oriented-portfolio/
└── README.md
```

**Note:** The capstone template often lists **`03_eda.ipynb`** separately; this repo’s EDA narrative spans **`02_cleaning.ipynb`** and **`04_statistical_analysis.ipynb`**. The PDF report’s appendix references the full five-notebook story for grading.

---

## Quick start

```bash
git clone https://github.com/adamyatiwari12/SectionD_G19_FlightOps-Dashboard.git
cd SectionD_G19_FlightOps-Dashboard
python3 scripts/etl_pipeline.py
python3 scripts/tableau_prep.py
```

---

## Team — Section D, Group 19

| Role | Member |
|------|--------|
| **Project Lead** | Adamya Tiwari |
| **Data Lead** | Prateek |
| **ETL Lead** | Yash Raghubanshi |
| **Visualization Lead** | Agnik Misra |
| **Analysis & Strategy Lead** | Rahul |
| **PPT Lead** | Ram |

Contribution matrix (P/S) vs Git history → **report §16** and **GitHub Insights**.

---

## Artifacts

| Asset | Link |
|--------|------|
| **Final report (PDF)** | [`reports/project_report.pdf`](reports/project_report.pdf) |
| **Presentation (PDF)** | [`reports/presentation.pdf`](reports/presentation.pdf) |
| **Tableau URLs + CSV map** | [`tableau/dashboard_links.md`](tableau/dashboard_links.md) |
| **Data dictionary** | [`docs/data_dictionary.md`](docs/data_dictionary.md) |

---

*Newton School of Technology · DVA Capstone 2 · All analysis is the team’s own work; cite the repo if you build on it.*
