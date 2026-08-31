import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(
    page_title="Nashville Urban Operations Intelligence Platform",
    page_icon="🏙️",
    layout="wide"
)


@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[1]

    data_file = (
        project_root
        / "data"
        / "processed"
        / "nashville_311_clean.csv"
    )

    dataframe = pd.read_csv(data_file)

    dataframe["Date_Time_Opened"] = pd.to_datetime(
        dataframe["Date_Time_Opened"],
        errors="coerce"
    )

    dataframe["Date_Time_Closed"] = pd.to_datetime(
        dataframe["Date_Time_Closed"],
        errors="coerce"
    )

    dataframe["Council_District"] = (
        dataframe["Council_District"]
        .astype("string")
        .str.replace(".0", "", regex=False)
        .str.zfill(2)
    )

    return dataframe


dataframe = load_data()


st.title("Nashville Urban Operations Intelligence Platform")

st.write(
    "Interactive analysis of Nashville 311 service requests."
)


# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filters")


# Request Type Filter
request_types = sorted(
    dataframe["Request_Type"]
    .dropna()
    .unique()
)

selected_request_type = st.sidebar.selectbox(
    "Request Type",
    ["All"] + request_types
)


# Status Filter
statuses = sorted(
    dataframe["Status"]
    .dropna()
    .unique()
)

selected_status = st.sidebar.selectbox(
    "Status",
    ["All"] + statuses
)


# Council District Filter
council_districts = sorted(
    dataframe["Council_District"]
    .dropna()
    .unique()
)

district_options = ["All"] + [
    f"District {district}"
    for district in council_districts
]

selected_district_option = st.sidebar.selectbox(
    "Council District",
    district_options
)


if selected_district_option == "All":
    selected_council_district = "All"
else:
    selected_council_district = (
        selected_district_option
        .replace("District ", "")
    )


# Date Range Filter
valid_dates = (
    dataframe["Date_Time_Opened"]
    .dropna()
)

minimum_date = valid_dates.min().date()
maximum_date = valid_dates.max().date()

selected_date_range = st.sidebar.date_input(
    "Date Range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)


# -----------------------------
# Apply Filters
# -----------------------------

filtered_dataframe = dataframe.copy()


if selected_request_type != "All":
    filtered_dataframe = filtered_dataframe[
        filtered_dataframe["Request_Type"]
        == selected_request_type
    ]


if selected_status != "All":
    filtered_dataframe = filtered_dataframe[
        filtered_dataframe["Status"]
        == selected_status
    ]


if selected_council_district != "All":
    filtered_dataframe = filtered_dataframe[
        filtered_dataframe["Council_District"]
        == selected_council_district
    ]


if len(selected_date_range) == 2:
    start_date = pd.Timestamp(selected_date_range[0])
    end_date = pd.Timestamp(selected_date_range[1])

    filtered_dataframe = filtered_dataframe[
        (
            filtered_dataframe["Date_Time_Opened"]
            >= start_date
        )
        &
        (
            filtered_dataframe["Date_Time_Opened"]
            < end_date + pd.Timedelta(days=1)
        )
    ]


# -----------------------------
# Dashboard Metrics
# -----------------------------

st.subheader("311 Service Request Overview")

column1, column2, column3 = st.columns(3)


with column1:
    st.metric(
        "Total Requests",
        len(filtered_dataframe)
    )


with column2:
    open_requests = (
        filtered_dataframe["Status"]
        .astype(str)
        .str.lower()
        .eq("open")
        .sum()
    )

    st.metric(
        "Open Requests",
        open_requests
    )


with column3:
    request_type_count = (
        filtered_dataframe["Request_Type"]
        .nunique()
    )

    st.metric(
        "Request Types",
        request_type_count
    )


st.divider()


# -----------------------------
# Requests Over Time
# -----------------------------

st.subheader("Requests Over Time")

requests_over_time = (
    filtered_dataframe
    .dropna(subset=["Date_Time_Opened"])
    .set_index("Date_Time_Opened")
    .resample("D")
    .size()
    .reset_index(name="Total Requests")
)

st.line_chart(
    requests_over_time,
    x="Date_Time_Opened",
    y="Total Requests"
)


st.divider()


# -----------------------------
# Requests by Type
# -----------------------------

st.subheader("Service Requests by Type")

request_type_counts = (
    filtered_dataframe["Request_Type"]
    .value_counts()
    .reset_index()
)

request_type_counts.columns = [
    "Request Type",
    "Total Requests"
]


st.bar_chart(
    request_type_counts,
    x="Request Type",
    y="Total Requests"
)


st.divider()


# -----------------------------
# Data Table
# -----------------------------

st.subheader("311 Service Request Data")


display_columns = [
    "Request__",
    "Status",
    "Request_Type",
    "Subrequest_Type",
    "City",
    "Council_District",
    "ZIP",
    "Date_Time_Opened",
    "Date_Time_Closed"
]


st.dataframe(
    filtered_dataframe[display_columns],
    use_container_width=True
)