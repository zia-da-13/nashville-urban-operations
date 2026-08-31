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

    return dataframe


dataframe = load_data()


st.title("Nashville Urban Operations Intelligence Platform")

st.write(
    "Interactive analysis of Nashville 311 service requests."
)


st.subheader("311 Service Request Overview")


column1, column2, column3 = st.columns(3)

with column1:
    st.metric(
        "Total Requests",
        len(dataframe)
    )

with column2:
    open_requests = (
        dataframe["Status"]
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
    request_types = dataframe["Request_Type"].nunique()

    st.metric(
        "Request Types",
        request_types
    )


st.divider()


st.subheader("Service Requests by Type")

request_type_counts = (
    dataframe["Request_Type"]
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
    dataframe[display_columns],
    use_container_width=True
)