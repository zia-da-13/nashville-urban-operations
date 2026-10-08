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
    page_title="Nashville WeGo Transit",
    page_icon="🚌",
    layout="wide"
)


# -----------------------------
# Load Transit Data
# -----------------------------

@st.cache_data
def load_transit_data():
    engine = get_database_engine()

    routes_query = text(
        "SELECT * FROM nashville_transit_routes"
    )

    stops_query = text(
        "SELECT * FROM nashville_transit_stops"
    )

    trips_query = text(
        "SELECT * FROM nashville_transit_trips"
    )

    with engine.connect() as connection:

        routes_dataframe = pd.read_sql(
            routes_query,
            connection
        )

        stops_dataframe = pd.read_sql(
            stops_query,
            connection
        )

        trips_dataframe = pd.read_sql(
            trips_query,
            connection
        )

    # -----------------------------
    # Clean Route IDs
    # -----------------------------

    routes_dataframe["Route_ID"] = (
        routes_dataframe["Route_ID"]
        .astype("string")
    )

    trips_dataframe["Route_ID"] = (
        trips_dataframe["Route_ID"]
        .astype("string")
    )

    # -----------------------------
    # Clean Stop Coordinates
    # -----------------------------

    stops_dataframe["Latitude"] = pd.to_numeric(
        stops_dataframe["Latitude"],
        errors="coerce"
    )

    stops_dataframe["Longitude"] = pd.to_numeric(
        stops_dataframe["Longitude"],
        errors="coerce"
    )

    return (
        routes_dataframe,
        stops_dataframe,
        trips_dataframe
    )


(
    routes_dataframe,
    stops_dataframe,
    trips_dataframe
) = load_transit_data()


# -----------------------------
# Header
# -----------------------------

st.title(
    "Nashville WeGo Transit Dashboard"
)

st.write(
    "Explore Nashville WeGo transit routes, "
    "stops, and scheduled trips."
)

st.caption(
    "Transit data is loaded from the WeGo "
    "GTFS feed and stored in the project "
    "SQLite database."
)


# -----------------------------
# Check Data
# -----------------------------

if routes_dataframe.empty:

    st.warning(
        "No transit route data is available."
    )

    st.stop()


# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header(
    "Transit Filters"
)


route_filter_dataframe = (
    routes_dataframe.copy()
)

route_filter_dataframe[
    "Route_Display"
] = (
    route_filter_dataframe[
        "Route_Number"
    ].fillna("")
    .astype(str)
    + " - "
    + route_filter_dataframe[
        "Route_Name"
    ].fillna("")
    .astype(str)
)


route_options = (
    route_filter_dataframe[
        "Route_Display"
    ]
    .dropna()
    .sort_values()
    .tolist()
)


selected_route = st.sidebar.selectbox(
    "Select Route",
    ["All Routes"] + route_options
)


# -----------------------------
# Determine Selected Route ID
# -----------------------------

selected_route_id = None


if selected_route != "All Routes":

    selected_route_record = (
        route_filter_dataframe[
            route_filter_dataframe[
                "Route_Display"
            ]
            == selected_route
        ]
    )

    if not selected_route_record.empty:

        selected_route_id = (
            selected_route_record.iloc[0][
                "Route_ID"
            ]
        )


# -----------------------------
# Filter Trips
# -----------------------------

filtered_trips_dataframe = (
    trips_dataframe.copy()
)


if selected_route_id is not None:

    filtered_trips_dataframe = (
        filtered_trips_dataframe[
            filtered_trips_dataframe[
                "Route_ID"
            ]
            == selected_route_id
        ]
    )


# -----------------------------
# Dashboard Metrics
# -----------------------------

st.subheader(
    "Transit Overview"
)

column1, column2, column3, column4 = (
    st.columns(4)
)


with column1:

    st.metric(
        "Transit Routes",
        f"{len(routes_dataframe):,}"
    )


with column2:

    st.metric(
        "Transit Stops",
        f"{len(stops_dataframe):,}"
    )


with column3:

    st.metric(
        "Scheduled Trips",
        f"{len(trips_dataframe):,}"
    )


with column4:

    if selected_route_id is None:

        active_route_count = (
            trips_dataframe[
                "Route_ID"
            ]
            .nunique()
        )

        st.metric(
            "Routes With Trips",
            f"{active_route_count:,}"
        )

    else:

        st.metric(
            "Selected Route Trips",
            f"{len(filtered_trips_dataframe):,}"
        )


st.divider()


# -----------------------------
# Selected Route Information
# -----------------------------

if selected_route_id is not None:

    st.subheader(
        "Selected Route"
    )

    selected_route_information = (
        route_filter_dataframe[
            route_filter_dataframe[
                "Route_ID"
            ]
            == selected_route_id
        ]
    )

    if not selected_route_information.empty:

        route_information = (
            selected_route_information.iloc[0]
        )

        route_column1, route_column2 = (
            st.columns(2)
        )

        with route_column1:

            st.metric(
                "Route Number",
                route_information[
                    "Route_Number"
                ]
            )

        with route_column2:

            st.metric(
                "Route Name",
                route_information[
                    "Route_Name"
                ]
            )

    st.divider()


# -----------------------------
# Transit Stop Map
# -----------------------------

st.subheader(
    "Nashville Transit Stop Map"
)

map_dataframe = (
    stops_dataframe[
        [
            "Stop_Name",
            "Latitude",
            "Longitude"
        ]
    ]
    .dropna(
        subset=[
            "Latitude",
            "Longitude"
        ]
    )
)


if not map_dataframe.empty:

    st.map(
        map_dataframe,
        latitude="Latitude",
        longitude="Longitude",
        zoom=10,
        use_container_width=True
    )

    st.caption(
        f"Mapped transit stops: "
        f"{len(map_dataframe):,}"
    )

else:

    st.info(
        "No transit stop coordinates "
        "are available."
    )


st.divider()


# -----------------------------
# Trips by Route
# -----------------------------

st.subheader(
    "Scheduled Trips by Route"
)

trips_by_route = (
    trips_dataframe
    .groupby(
        "Route_ID"
    )
    .size()
    .reset_index(
        name="Scheduled_Trips"
    )
)


trips_by_route = (
    trips_by_route.merge(
        routes_dataframe[
            [
                "Route_ID",
                "Route_Number",
                "Route_Name"
            ]
        ],
        on="Route_ID",
        how="left"
    )
)


trips_by_route[
    "Route"
] = (
    trips_by_route[
        "Route_Number"
    ].fillna("")
    .astype(str)
    + " - "
    + trips_by_route[
        "Route_Name"
    ].fillna("")
    .astype(str)
)


trips_by_route = (
    trips_by_route.sort_values(
        by="Scheduled_Trips",
        ascending=False
    )
    .head(15)
)


if not trips_by_route.empty:

    st.bar_chart(
        trips_by_route,
        x="Route",
        y="Scheduled_Trips"
    )

else:

    st.info(
        "No scheduled trip information "
        "is available."
    )


st.divider()


# -----------------------------
# Trip Direction Analysis
# -----------------------------

st.subheader(
    "Trip Directions"
)

direction_counts = (
    filtered_trips_dataframe[
        "Direction_ID"
    ]
    .fillna("Unknown")
    .astype(str)
    .value_counts()
    .reset_index()
)

direction_counts.columns = [
    "Direction",
    "Scheduled Trips"
]


if not direction_counts.empty:

    st.bar_chart(
        direction_counts,
        x="Direction",
        y="Scheduled Trips"
    )

else:

    st.info(
        "No trip direction information "
        "is available."
    )


st.divider()


# -----------------------------
# Transit Routes Table
# -----------------------------

st.subheader(
    "WeGo Transit Routes"
)

route_display_columns = [
    "Route_ID",
    "Route_Number",
    "Route_Name",
    "Route_Type"
]


st.dataframe(
    routes_dataframe[
        route_display_columns
    ],
    use_container_width=True
)


st.divider()


# -----------------------------
# Transit Stops Table
# -----------------------------

st.subheader(
    "WeGo Transit Stops"
)

stop_search = st.text_input(
    "Search for a transit stop"
)


filtered_stops_dataframe = (
    stops_dataframe.copy()
)


if stop_search:

    filtered_stops_dataframe = (
        filtered_stops_dataframe[
            filtered_stops_dataframe[
                "Stop_Name"
            ]
            .astype(str)
            .str.contains(
                stop_search,
                case=False,
                na=False
            )
        ]
    )


stop_display_columns = [
    "Stop_ID",
    "Stop_Name",
    "Latitude",
    "Longitude"
]


st.dataframe(
    filtered_stops_dataframe[
        stop_display_columns
    ],
    use_container_width=True
)


st.divider()


# -----------------------------
# Scheduled Trips Table
# -----------------------------

st.subheader(
    "Scheduled Transit Trips"
)

trip_display_columns = [
    "Route_ID",
    "Service_ID",
    "Trip_ID",
    "Trip_Headsign",
    "Direction_ID"
]


st.dataframe(
    filtered_trips_dataframe[
        trip_display_columns
    ],
    use_container_width=True
)