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
    page_title="Nashville Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)


# -----------------------------
# Load Weather Data
# -----------------------------

@st.cache_data
def load_weather_data():
    engine = get_database_engine()

    query = text(
        "SELECT * FROM nashville_weather"
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(
            query,
            connection
        )

    dataframe["Start_Time"] = pd.to_datetime(
        dataframe["Start_Time"],
        errors="coerce"
    )

    dataframe["End_Time"] = pd.to_datetime(
        dataframe["End_Time"],
        errors="coerce"
    )

    numeric_columns = [
        "Temperature",
        "Precipitation_Probability",
        "Wind_Speed_MPH"
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    dataframe = dataframe.sort_values(
        by="Start_Time"
    )

    return dataframe


weather_dataframe = load_weather_data()


# -----------------------------
# Header
# -----------------------------

st.title(
    "Nashville Weather Forecast"
)

st.write(
    "Hourly weather forecast for Nashville, Tennessee."
)

st.caption(
    "Weather data stored in the Nashville weather SQLite table."
)


# -----------------------------
# Check Data
# -----------------------------

if weather_dataframe.empty:

    st.warning(
        "No weather forecast data is available."
    )

    st.stop()


# -----------------------------
# Current Forecast Record
# -----------------------------

current_forecast = weather_dataframe.iloc[0]


# -----------------------------
# Overview Metrics
# -----------------------------

st.subheader(
    "Weather Overview"
)

column1, column2, column3, column4 = st.columns(4)


with column1:

    temperature = current_forecast[
        "Temperature"
    ]

    temperature_unit = current_forecast[
        "Temperature_Unit"
    ]

    if pd.notna(temperature):

        st.metric(
            "Temperature",
            f"{int(temperature)}°{temperature_unit}"
        )

    else:

        st.metric(
            "Temperature",
            "N/A"
        )


with column2:

    precipitation = current_forecast[
        "Precipitation_Probability"
    ]

    if pd.notna(precipitation):

        st.metric(
            "Precipitation",
            f"{int(precipitation)}%"
        )

    else:

        st.metric(
            "Precipitation",
            "N/A"
        )


with column3:

    wind_speed = current_forecast[
        "Wind_Speed_MPH"
    ]

    if pd.notna(wind_speed):

        st.metric(
            "Wind Speed",
            f"{int(wind_speed)} mph"
        )

    else:

        st.metric(
            "Wind Speed",
            "N/A"
        )


with column4:

    forecast_condition = current_forecast[
        "Short_Forecast"
    ]

    if pd.notna(forecast_condition):

        st.metric(
            "Conditions",
            forecast_condition
        )

    else:

        st.metric(
            "Conditions",
            "N/A"
        )


st.divider()


# -----------------------------
# Forecast Time
# -----------------------------

st.subheader(
    "Forecast Period"
)

forecast_start = current_forecast[
    "Start_Time"
]

forecast_end = current_forecast[
    "End_Time"
]

st.write(
    f"Forecast begins: **{forecast_start}**"
)

st.write(
    f"Forecast ends: **{forecast_end}**"
)


st.divider()


# -----------------------------
# Temperature Forecast
# -----------------------------

st.subheader(
    "Hourly Temperature Forecast"
)

temperature_chart_data = weather_dataframe[
    [
        "Start_Time",
        "Temperature"
    ]
].dropna()


if not temperature_chart_data.empty:

    st.line_chart(
        temperature_chart_data,
        x="Start_Time",
        y="Temperature"
    )

else:

    st.info(
        "No temperature forecast data is available."
    )


st.divider()


# -----------------------------
# Precipitation Forecast
# -----------------------------

st.subheader(
    "Precipitation Probability"
)

precipitation_chart_data = weather_dataframe[
    [
        "Start_Time",
        "Precipitation_Probability"
    ]
].dropna()


if not precipitation_chart_data.empty:

    st.line_chart(
        precipitation_chart_data,
        x="Start_Time",
        y="Precipitation_Probability"
    )

else:

    st.info(
        "No precipitation forecast data is available."
    )


st.divider()


# -----------------------------
# Wind Speed Forecast
# -----------------------------

st.subheader(
    "Wind Speed Forecast"
)

wind_chart_data = weather_dataframe[
    [
        "Start_Time",
        "Wind_Speed_MPH"
    ]
].dropna()


if not wind_chart_data.empty:

    st.line_chart(
        wind_chart_data,
        x="Start_Time",
        y="Wind_Speed_MPH"
    )

else:

    st.info(
        "No wind speed forecast data is available."
    )


st.divider()


# -----------------------------
# Forecast Conditions
# -----------------------------

st.subheader(
    "Forecast Conditions"
)

condition_counts = (
    weather_dataframe[
        "Short_Forecast"
    ]
    .dropna()
    .value_counts()
    .reset_index()
)

condition_counts.columns = [
    "Forecast Condition",
    "Hours"
]


if not condition_counts.empty:

    st.bar_chart(
        condition_counts,
        x="Forecast Condition",
        y="Hours"
    )

else:

    st.info(
        "No forecast conditions are available."
    )


st.divider()


# -----------------------------
# Weather Data Table
# -----------------------------

st.subheader(
    "Hourly Weather Forecast Data"
)

display_columns = [
    "Start_Time",
    "End_Time",
    "Temperature",
    "Temperature_Unit",
    "Precipitation_Probability",
    "Wind_Speed_MPH",
    "Wind_Direction",
    "Short_Forecast"
]


st.dataframe(
    weather_dataframe[
        display_columns
    ],
    use_container_width=True
)