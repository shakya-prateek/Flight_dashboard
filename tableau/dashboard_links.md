# ✈️ Tableau Dashboards — US Flight Delay Analysis (2015)

## 🔗 Published Dashboards

| Dashboard | Link |
|----------|------|
| Operations Overview | *https://public.tableau.com/views/OperationsDashboard_17774656392980/OperationsOverview?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link* |
| Delay & Performance Analysis | *https://public.tableau.com/views/DelayDashboard_17774660273340/DelayAnalysis?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link* |
| Route & Airport Analysis | *https://public.tableau.com/views/RouteAirportDashboard/RouteAirport?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link* |
| Airline Performance Comparison | *https://public.tableau.com/views/AirlineDashboard_17774679517270/AIRLINECOMPARISON?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link* |

---

## 📊 Project Overview

This project analyzes US flight operations in 2015 through **four separate Tableau dashboards**, each focusing on a different aspect of airline performance — from high-level KPIs to deep operational insights.

---

## 🧭 Dashboard 1 — Operations Overview

### 🎯 Purpose:
Provides a **high-level snapshot** of overall flight operations.

### Key Components:
- KPI Scorecards:
  - Total Flights  
  - On-Time %  
  - Avg Departure Delay  
  - Cancellation Rate  

- Monthly flight trends  
- Delay distribution (Early, 0–15, 15–60, 60+)  
- Flights by day of week  

### 💡 Insight Focus:
- Overall operational stability  
- Frequency and distribution of delays  

---

## ⏱ Dashboard 2 — Delay & Performance Analysis

### 🎯 Purpose:
Analyzes **patterns and causes of delays**

### Key Components:
- Departure vs Arrival delay (scatter plot)  
- Delay by time of day  
- Delay cause breakdown:
  - Airline  
  - Weather  
  - Air System  
  - Late Aircraft  

### 💡 Insight Focus:
- How delays propagate  
- Root causes of delays  

---

## 🌍 Dashboard 3 — Route & Airport Analysis

### 🎯 Purpose:
Examines **geographic and route-level performance**

### Key Components:
- Airport map (flight density)  
- Top routes by traffic  
- Avg delay by airport  

### 💡 Insight Focus:
- Busiest airports and hubs  
- High-traffic routes  
- Delay bottlenecks  

---

## 🏢 Dashboard 4 — Airline Performance Comparison

### 🎯 Purpose:
Compares airlines across key performance metrics

### Key Components:
- On-Time % by airline  
- Avg delay by airline  
- Cancellation rate  
- Flight volume  

### 💡 Insight Focus:
- Best and worst performing airlines  
- Trade-off between volume and efficiency  

---

## 🗂 Data Sources Used

| Tableau Data Source | File |
|---|---|
| Airline Summary | `data/processed/tableau/tableau_airline_summary.csv` |
| Airport Summary | `data/processed/tableau/tableau_airport_summary.csv` |
| Monthly Trends | `data/processed/tableau/tableau_monthly_trends.csv` |
| Route Analysis | `data/processed/tableau/tableau_route_analysis.csv` |
| Delay Causes | `data/processed/tableau/tableau_delay_causes.csv` |
| Hourly Patterns | `data/processed/tableau/tableau_hourly_pattern.csv` |
| Flight Sample | `data/processed/tableau/tableau_flights_sample.csv` |

---

## 🖼 Screenshots

Screenshots of the dashboards are available in:  
`tableau/screenshots/`

---

## 💡 Notes

- Each dashboard is designed as a **standalone analytical view**  
- Together, they form a **complete analysis pipeline**:
  - Overview → Delay Analysis → Geographic Insights → Airline Comparison  
