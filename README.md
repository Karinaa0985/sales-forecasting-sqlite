# 📊 Retail Sales Analytics & Demand Forecasting Pipeline

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sales-forecasting-app-blcfmnmcp7t8uj9jbnexm7.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

An end-to-end data engineering, analytics, and time-series forecasting pipeline built with **Python**, **SQLite**, and **Streamlit**. 

This project transforms raw transactional retail data into an indexed relational database, executes complex analytical SQL queries (CTEs, Window Functions, dynamic aggregations), generates demand forecasts, and serves an interactive live dashboard.

🚀 **Live Interactive App:** [sales-forecasting-app-blcfmnmcp7t8uj9jbnexm7.streamlit.app](https://sales-forecasting-app-blcfmnmcp7t8uj9jbnexm7.streamlit.app/)

---

## 🚀 Key Features & Architecture

* **Automated ETL Pipeline (`build_db.py`):** Ingests raw Excel/CSV transactional data, normalizes heterogeneous column headers, and builds an optimized relational database schema in SQLite.
* **Relational Database Engine (`superstore.db`):** Houses raw transactional records (`sales_raw`) and aggregated analytical data views (`monthly_sales_summary`).
* **Advanced SQL Analytics:** Utilizes **CTEs, `GROUP BY` aggregations, and Window Functions (`OVER PARTITION BY`)** to compute monthly revenue, order totals, and rolling 3-month average sales trends.
* **Time-Series Demand Forecasting:** Runs moving average and trend projection models in Python, writing generated forecast outputs directly back to the SQLite `sales_forecasts` table.
* **Interactive Cloud Dashboard (`app.py`):** Deployed on **Streamlit Cloud**, featuring interactive filtering by product category and region, KPI summary metrics, dynamic charts, and an embedded **SQL Query Explorer**.

---

## 📂 Repository Structure

```text
sales-forecasting-sqlite/
│
├── data/                      # Raw input datasets (Superstore.xls / CSV)
├── database/
│   ├── build_db.py            # Automated ETL script to build SQLite database
│   └── superstore.db          # Embedded SQLite database
│
├── notebooks/
│   └── sales_analysis.ipynb   # Jupyter notebook containing SQL queries & forecasting logic
│
├── app.py                     # Interactive Streamlit dashboard application
├── requirements.txt           # Python environment dependencies
└── README.md                  # Project documentation
