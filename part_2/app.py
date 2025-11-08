# Importing necessary libraries
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# DARK THEME:
# Changes to dark theme (default is white).
plt.style.use("dark_background")

# PAGE SETUP:
# Set up page title, layout, and basic style.
st.set_page_config(page_title="YH Programs Dashboard", layout="wide")

# CSS tweaks to tighten layout spacing and styling.
st.markdown(
    """
    <style>
        /* Subtle tighten-ups */
        .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        h1 {margin-bottom: .25rem;}
        .metric {text-align:center;}
    </style>
    """,
    unsafe_allow_html=True,
)

# DATA:
@st.cache_data # Caches loaded data so it doesn’t reload every time you interact with filters.
def load_data(csv_name: str) -> pd.DataFrame:
    """
    Load CSV file into a pandas DataFrame.
    - Uses Path to locate the file.
    - Converts some columns to numeric types for consistency.
    - Caches the data so it loads faster on re-runs.
    """
    p = Path(csv_name)
    if not p.exists():
        p = Path(__file__).parent / csv_name
    df = pd.read_csv(p)


    # Convert relevant columns to numeric values if they exist.
    if "Multiple Municipalities" in df.columns:
        df["Multiple Municipalities"] = pd.to_numeric(df["Multiple Municipalities"], errors="coerce").fillna(0).astype("int64")
    if "YH Points" in df.columns:
        df["YH Points"] = pd.to_numeric(df["YH Points"], errors="coerce")
    if "Study Weeks" in df.columns:
        df["Study Weeks"] = pd.to_numeric(df["Study Weeks"], errors="coerce")
    if "Study Years" in df.columns:
        df["Study Years"] = pd.to_numeric(df["Study Years"], errors="coerce")
    return df

# Load the harmonized dataset.
df = load_data("harmonized_yh_2020_2022.csv")

# PAGE TITLE:
st.title("YH Education Programs Dashboard")
st.caption("Explore approved programs across years, fields and regions.")

# SIDEBAR FILTERS:
# The sidebar allows users to filter the data.
with st.sidebar:
    st.header("Filters")
    years   = st.multiselect("Year", sorted(df["Year"].dropna().unique()), default=sorted(df["Year"].dropna().unique()))
    fields  = st.multiselect("Education Field", sorted(df["Education Field"].dropna().unique()))
    counties = st.multiselect("County", sorted(df["County"].dropna().unique()))
    text    = st.text_input("Search program/provider", placeholder="e.g. Java, Stockholm, Jensen")

# Apply filters to the dataset.
f = df.copy()
if years:   f = f[f["Year"].isin(years)]
if fields:  f = f[f["Education Field"].isin(fields)]
if counties:f = f[f["County"].isin(counties)]
if text:
    t = text.strip().lower()
    cols = ["Program Name", "Provider Admin Unit", "County", "Municipality", "Education Field"]
    f = f[f[cols].astype(str).apply(lambda s: s.str.lower().str.contains(t)).any(axis=1)]

# KPIs:
# Quick overview of the filtered data at the top of the dashboard.
c1, c2, c3, c4 = st.columns(4)
c1.metric("Programs", f"{len(f):,}")
c2.metric("Providers", f"{f['Provider Admin Unit'].nunique():,}")
c3.metric("Avg YH Points", f"{int(f['YH Points'].mean()) if not f.empty else 0}")
c4.metric("Avg Duration (weeks)", f"{int(f['Study Weeks'].mean()) if 'Study Weeks' in f.columns and not f.empty else 0}")

# Create Tabs for organization .
tab1, tab2, tab3 = st.tabs(["Overview", "By Field / County", "Data"])

# Tab 1: Overview cards & charts
with tab1:
    left, right = st.columns([2, 1]) # Splits the screen into two chart columns.

    # Left chart: Programs per Education Field.
    with left:
        st.subheader("Programs by Education Field")
        counts = f["Education Field"].value_counts().head(12)
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("Programs")
        ax.set_xlabel("")
        st.pyplot(fig, use_container_width=True)

    # Right chart: Distribution of YH Points.
    with right:
        st.subheader("Distribution of YH Points")
        fig2, ax2 = plt.subplots()
        f["YH Points"].dropna().plot(kind="hist", bins=20, ax=ax2)
        ax2.set_xlabel("YH Points")
        ax2.set_ylabel("Count")
        st.pyplot(fig2, use_container_width=True)

    # Table of Top programs
    st.markdown("---")
    st.subheader("Top Programs by YH Points")
    top_n = st.slider("Show top N", 5, 50, 15, key="topn")
    st.dataframe(
        f.sort_values("YH Points", ascending=False)
        .loc[:, ["Year", "Education Field", "Program Name", "County", "Municipality", "YH Points", "Provider Admin Unit"]]
        .head(top_n),
        use_container_width=True
    )

# TAB 2: Aggregations (Comparisons across groups).
with tab2:
    colA, colB = st.columns(2)

    # Average YH Points by County.
    with colA:
        st.subheader("Avg YH Points by County (top 20)")
        avg = f.groupby("County")["YH Points"].mean().sort_values(ascending=False).head(20)
        fig3, ax3 = plt.subplots()
        avg.plot(kind="bar", ax=ax3)
        ax3.set_ylabel("Avg YH Points")
        ax3.set_xlabel("")
        st.pyplot(fig3, use_container_width=True)

    # Average YH Points by Education Field.
    with colB:
        st.subheader("Avg YH Points by Education Field")
        avg_field = f.groupby("Education Field")["YH Points"].mean().sort_values(ascending=False)
        fig4, ax4 = plt.subplots()
        avg_field.plot(kind="bar", ax=ax4)w
        ax4.set_ylabel("Avg YH Points")
        ax4.set_xlabel("")
        st.pyplot(fig4, use_container_width=True)

# TAB 3: Display raw filtered data + download
with tab3:
    st.subheader("Filtered Data")
    st.dataframe(f, use_container_width=True, height=450)

    # Add a button to export filtered data
    csv = f.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", csv, "filtered_yh.csv", "text/csv")