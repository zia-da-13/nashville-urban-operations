import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from sqlalchemy import text


# -----------------------------
# Project Path Setup
# -----------------------------

project_root = Path(__file__).resolve().parents[2]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from src.database.database_connection import get_database_engine


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Nashville Public Safety",
    page_icon="🚔",
    layout="wide"
)


# -----------------------------
# Load Crime Data
# -----------------------------

@st.cache_data
def load_crime_data():
    engine = get_database_engine()

    query = text(
        "SELECT * FROM nashville_crime"
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(
            query,
            connection
        )

    dataframe["Incident_Occurred"] = pd.to_datetime(
        dataframe["Incident_Occurred"],
        errors="coerce"
    )

    dataframe["Incident_Reported"] = pd.to_datetime(
        dataframe["Incident_Reported"],
        errors="coerce"
    )

    dataframe["Latitude"] = pd.to_numeric(
        dataframe["Latitude"],
        errors="coerce"
    )

    dataframe["Longitude"] = pd.to_numeric(
        dataframe["Longitude"],
        errors="coerce"
    )

    dataframe["ZIP_Code"] = (
        dataframe["ZIP_Code"]
        .astype("string")
        .str.replace(".0", "", regex=False)
    )

    return dataframe


crime_dataframe = load_crime_data()


# -----------------------------
# Header
# -----------------------------

st.title(
    "Nashville Public Safety Dashboard"
)

st.write(
    "Interactive analysis of Metro Nashville "
    "Police Department incident records."
)

st.caption(
    "Data source: Nashville police incident data "
    "stored in the project SQLite database."
)


# -----------------------------
# Check Data
# -----------------------------

if crime_dataframe.empty:

    st.warning(
        "No public safety data is available."
    )

    st.stop()


# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header(
    "Public Safety Filters"
)


# -----------------------------
# Offense Filter
# -----------------------------

offense_types = sorted(
    crime_dataframe["Offense_Description"]
    .dropna()
    .unique()
)

selected_offense = st.sidebar.selectbox(
    "Offense",
    ["All"] + offense_types
)


# -----------------------------
# Investigation Status Filter
# -----------------------------

investigation_statuses = sorted(
    crime_dataframe["Investigation_Status"]
    .dropna()
    .unique()
)

selected_investigation_status = (
    st.sidebar.selectbox(
        "Investigation Status",
        ["All"] + investigation_statuses
    )
)


# -----------------------------
# ZIP Code Filter
# -----------------------------

zip_codes = sorted(
    crime_dataframe["ZIP_Code"]
    .dropna()
    .unique()
)

selected_zip_code = st.sidebar.selectbox(
    "ZIP Code",
    ["All"] + zip_codes
)


# -----------------------------
# Date Range Filter
# -----------------------------

valid_dates = (
    crime_dataframe["Incident_Occurred"]
    .dropna()
)

minimum_date = valid_dates.min().date()
maximum_date = valid_dates.max().date()

selected_date_range = st.sidebar.date_input(
    "Incident Date Range",
    value=(
        minimum_date,
        maximum_date
    ),
    min_value=minimum_date,
    max_value=maximum_date
)


# -----------------------------
# Apply Filters
# -----------------------------

filtered_dataframe = (
    crime_dataframe.copy()
)


if selected_offense != "All":

    filtered_dataframe = (
        filtered_dataframe[
            filtered_dataframe[
                "Offense_Description"
            ]
            == selected_offense
        ]
    )


if selected_investigation_status != "All":

    filtered_dataframe = (
        filtered_dataframe[
            filtered_dataframe[
                "Investigation_Status"
            ]
            == selected_investigation_status
        ]
    )


if selected_zip_code != "All":

    filtered_dataframe = (
        filtered_dataframe[
            filtered_dataframe[
                "ZIP_Code"
            ]
            == selected_zip_code
        ]
    )


if len(selected_date_range) == 2:

    start_date = pd.Timestamp(
        selected_date_range[0]
    )

    end_date = pd.Timestamp(
        selected_date_range[1]
    )

    filtered_dataframe = (
        filtered_dataframe[
            (
                filtered_dataframe[
                    "Incident_Occurred"
                ]
                >= start_date
            )
            &
            (
                filtered_dataframe[
                    "Incident_Occurred"
                ]
                < end_date
                + pd.Timedelta(days=1)
            )
        ]
    )


# -----------------------------
# Overview Metrics
# -----------------------------

st.subheader(
    "Public Safety Overview"
)

column1, column2, column3, column4 = (
    st.columns(4)
)


with column1:

    st.metric(
        "Total Records",
        f"{len(filtered_dataframe):,}"
    )


with column2:

    unique_incidents = (
        filtered_dataframe[
            "Incident_Number"
        ]
        .nunique()
    )

    st.metric(
        "Unique Incidents",
        f"{unique_incidents:,}"
    )


with column3:

    open_investigations = (
        filtered_dataframe[
            "Investigation_Status"
        ]
        .astype(str)
        .str.lower()
        .eq("open")
        .sum()
    )

    st.metric(
        "Open Records",
        f"{open_investigations:,}"
    )


with column4:

    domestic_values = (
        filtered_dataframe[
            "Domestic_Related"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    domestic_records = (
        domestic_values
        .isin(
            [
                "yes",
                "y",
                "true",
                "1"
            ]
        )
        .sum()
    )

    st.metric(
        "Domestic-Related Records",
        f"{domestic_records:,}"
    )


st.divider()


# -----------------------------
# Incident Map
# -----------------------------

st.subheader(
    "Public Safety Incident Map"
)

map_dataframe = (
    filtered_dataframe[
        [
            "Latitude",
            "Longitude"
        ]
    ]
    .dropna()
)


if not map_dataframe.empty:

    st.map(
        map_dataframe,
        latitude="Latitude",
        longitude="Longitude",
        use_container_width=True
    )

    st.caption(
        f"Mapped records: "
        f"{len(map_dataframe):,}"
    )

else:

    st.info(
        "No geographic locations are available "
        "for the selected filters."
    )


st.divider()


# -----------------------------
# Incidents Over Time
# -----------------------------

st.subheader(
    "Incident Records Over Time"
)

incidents_over_time = (
    filtered_dataframe
    .dropna(
        subset=["Incident_Occurred"]
    )
    .set_index("Incident_Occurred")
    .resample("D")
    .size()
    .reset_index(
        name="Total Records"
    )
)


if not incidents_over_time.empty:

    st.line_chart(
        incidents_over_time,
        x="Incident_Occurred",
        y="Total Records"
    )

else:

    st.info(
        "No incident records are available "
        "for the selected date range."
    )


st.divider()


# -----------------------------
# Offenses by Type
# -----------------------------

st.subheader(
    "Records by Offense Type"
)

offense_counts = (
    filtered_dataframe[
        "Offense_Description"
    ]
    .dropna()
    .value_counts()
    .head(15)
    .reset_index()
)

offense_counts.columns = [
    "Offense",
    "Total Records"
]


if not offense_counts.empty:

    st.bar_chart(
        offense_counts,
        x="Offense",
        y="Total Records"
    )

else:

    st.info(
        "No offense data is available "
        "for the selected filters."
    )


st.divider()


# -----------------------------
# Investigation Status
# -----------------------------

st.subheader(
    "Investigation Status"
)

status_counts = (
    filtered_dataframe[
        "Investigation_Status"
    ]
    .dropna()
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Investigation Status",
    "Total Records"
]


if not status_counts.empty:

    st.bar_chart(
        status_counts,
        x="Investigation Status",
        y="Total Records"
    )

else:

    st.info(
        "No investigation status data "
        "is available."
    )


st.divider()


# -----------------------------
# Domestic-Related Records
# -----------------------------

st.subheader(
    "Domestic-Related Records"
)

domestic_counts = (
    filtered_dataframe[
        "Domestic_Related"
    ]
    .fillna("Unknown")
    .astype(str)
    .value_counts()
    .reset_index()
)

domestic_counts.columns = [
    "Domestic Related",
    "Total Records"
]


if not domestic_counts.empty:

    st.bar_chart(
        domestic_counts,
        x="Domestic Related",
        y="Total Records"
    )


st.divider()


# -----------------------------
# Public Safety Data Table
# -----------------------------

st.subheader(
    "Public Safety Incident Data"
)

display_columns = [
    "Incident_Number",
    "Incident_Occurred",
    "Incident_Reported",
    "Offense_Description",
    "Incident_Status",
    "Investigation_Status",
    "Domestic_Related",
    "Weapon_Description",
    "Location_Type",
    "ZIP_Code",
    "Latitude",
    "Longitude"
]


st.dataframe(
    filtered_dataframe[
        display_columns
    ],
    use_container_width=True
)