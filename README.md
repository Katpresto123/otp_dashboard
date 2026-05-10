[README.md](https://github.com/user-attachments/files/27571040/README.md)
# TriMet On-Time Performance Analysis
**Portland State University | M.S. Applied Data Science for Business | Capstone Project**

## Overview
This project analyzes on-time performance (OTP) across the TriMet public transit system in Portland, Oregon. Using three years of stop-level operational data (2022–2024), we identified systemic patterns in bus delays and delivered actionable recommendations to TriMet leadership.

**The core finding:** On-time departure does not equal a reliable trip. Delays accumulate mid-route — and the data shows exactly where, when, and why.

---

## Key Findings
- **12M+ transit records** analyzed across 3 years of stop-level data
- **10 buses** out of 85 active units accounted for 20%+ of all in-service failures
- **Route 293** showed a 10-point OTP drop with ramp deployment — an accessibility issue hidden in the data
- **Peak hours** consistently ran 5–6% lower OTP than off-peak across the entire system
- **SE 82nd & King** underperformed in every sign-up period across all three years
- **Powell Garage** consistently outperformed other garages — used as an operational benchmark

---

## Methods
- K-Means Clustering
- DBSCAN
- Random Forest
- Logistic Regression
- Chi-Square Hypothesis Testing
- Geospatial Analysis & Interactive Mapping
- Sentiment Analysis (rider survey data)
- Dwell Time & Load Analysis

---

## Project Structure
```
otp_dashboard/
├── gtfs_dashboard.ipynb        # Main analysis notebook
├── otp_dashboard.py            # Dashboard script
├── otp_dashboard_v1.py         # Dashboard script v1
├── stop_times.zip              # Stop-level timing data
├── stops.txt                   # Stop location data
├── routes.txt                  # Route metadata
├── trips.txt                   # Trip-level records
├── shapes.txt                  # Geographic route shapes
├── requirements.txt            # Dependencies
└── README.md
```

---

## Tools & Libraries
- Python, Pandas, NumPy
- Scikit-learn (clustering, regression, random forest)
- Matplotlib, Seaborn
- Folium (interactive maps)
- Jupyter Notebook

---

## Data Source
Data sourced from [TriMet's public GTFS feed](https://developer.trimet.org/) and internal operational records provided through the PSU capstone partnership.

---

## Recommendations Delivered to TriMet
1. **Operator Training** — Targeted pacing and timepoint management training for high-variability routes
2. **Ramp-Delay Buffers** — Schedule padding adjustments for accessibility stops, prioritizing Route 293
3. **Adaptive Scheduling** — Segment-level time adjustments on deviation-prone corridors
4. **Predictive Fleet Maintenance** — Flag top 10 failure-prone buses for proactive maintenance before peak season
5. **Data Governance** — Audit and resolve anomalous stop data (e.g., Stop ID 13568 with zero OTP across all years)

---

## Team
Kathy Presto · Angrich Brophy · Floren Lebaron · David Alsalemi
Portland State University — June 2025

---

## Contact
[LinkedIn](https://linkedin.com/in/k-presto)
