# Data Transformation & Visualization

A data engineering project built in Python, using pandas, Jupyter Notebooks, and Streamlit.

This was my **third Python lab**, built during the course *Programmering i Python* in November 2025. The project focuses on ETL (Extract, Transform, Load) — taking real-world messy data, harmonizing it, and visualizing it in an interactive dashboard.

## What it does

- **Part 1** — Pandas exercises using a Kickstarter dataset
- **Part 2** — Full ETL pipeline on Swedish vocational education (YH) application data from 2020–2022:
  - Explores and analyzes raw Excel datasets
  - Harmonizes and cleans data across multiple years with different structures
  - Enriches the dataset with additional columns
  - Exports a clean, unified CSV
  - Visualizes the data in an interactive Streamlit dashboard

## How to run

```bash
pip install -r part_2/requirements.txt
```

**Notebook (data transformation):**
Open `part_2/data_transform.ipynb` in Jupyter and run top to bottom.

**Streamlit dashboard:**
```bash
streamlit run part_2/app.py
```

## Structure

- `part_1/` — Pandas practice notebook with Kickstarter data
- `part_2/data_transform.ipynb` — Full transformation pipeline
- `part_2/app.py` — Streamlit dashboard
- `part_2/harmonized_yh_2020_2022.csv` — Final cleaned dataset
- `part_2/resultat-ansokningsomgang-*.xlsx` — Raw source data (2020–2022)

## Tech

- Python 3
- pandas
- Streamlit
- Jupyter Notebook
- plotly / matplotlib
