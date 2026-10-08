import pandas as pd
from pathlib import Path


def transform_nashville_transit():
    project_root = Path(__file__).resolve().parents[2]

    raw_folder = (
        project_root
        / "data"
        / "raw"
        / "nashville_transit"
    )

    processed_folder = (
        project_root
        / "data"
        / "processed"
        / "nashville_transit"
    )

    processed_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------
    # File Paths
    # -----------------------------

    routes_file = (
        raw_folder
        / "routes.txt"
    )

    stops_file = (
        raw_folder
        / "stops.txt"
    )

    trips_file = (
        raw_folder
        / "trips.txt"
    )

    # -----------------------------
    # Load GTFS Data
    # -----------------------------

    print(
        "Loading WeGo transit data..."
    )

    routes_dataframe = pd.read_csv(
        routes_file,
        dtype=str
    )

    stops_dataframe = pd.read_csv(
        stops_file,
        dtype=str
    )

    trips_dataframe = pd.read_csv(
        trips_file,
        dtype=str
    )

    print()

    print(
        f"Routes loaded: "
        f"{len(routes_dataframe)}"
    )

    print(
        f"Stops loaded: "
        f"{len(stops_dataframe)}"
    )

    print(
        f"Trips loaded: "
        f"{len(trips_dataframe)}"
    )

    # -----------------------------
    # Display Original Columns
    # -----------------------------

    print()
    print("Routes columns:")
    print(
        routes_dataframe.columns.tolist()
    )

    print()
    print("Stops columns:")
    print(
        stops_dataframe.columns.tolist()
    )

    print()
    print("Trips columns:")
    print(
        trips_dataframe.columns.tolist()
    )

    # -----------------------------
    # Transform Routes
    # -----------------------------

    route_columns = [
        "route_id",
        "route_short_name",
        "route_long_name",
        "route_type"
    ]

    available_route_columns = [
        column
        for column in route_columns
        if column in routes_dataframe.columns
    ]

    cleaned_routes_dataframe = (
        routes_dataframe[
            available_route_columns
        ].copy()
    )

    cleaned_routes_dataframe = (
        cleaned_routes_dataframe
        .drop_duplicates(
            subset=["route_id"]
        )
    )

    cleaned_routes_dataframe = (
        cleaned_routes_dataframe.rename(
            columns={
                "route_id": "Route_ID",
                "route_short_name": "Route_Number",
                "route_long_name": "Route_Name",
                "route_type": "Route_Type"
            }
        )
    )

    # -----------------------------
    # Transform Stops
    # -----------------------------

    stop_columns = [
        "stop_id",
        "stop_name",
        "stop_lat",
        "stop_lon"
    ]

    available_stop_columns = [
        column
        for column in stop_columns
        if column in stops_dataframe.columns
    ]

    cleaned_stops_dataframe = (
        stops_dataframe[
            available_stop_columns
        ].copy()
    )

    cleaned_stops_dataframe = (
        cleaned_stops_dataframe
        .drop_duplicates(
            subset=["stop_id"]
        )
    )

    cleaned_stops_dataframe[
        "stop_lat"
    ] = pd.to_numeric(
        cleaned_stops_dataframe[
            "stop_lat"
        ],
        errors="coerce"
    )

    cleaned_stops_dataframe[
        "stop_lon"
    ] = pd.to_numeric(
        cleaned_stops_dataframe[
            "stop_lon"
        ],
        errors="coerce"
    )

    cleaned_stops_dataframe = (
        cleaned_stops_dataframe.rename(
            columns={
                "stop_id": "Stop_ID",
                "stop_name": "Stop_Name",
                "stop_lat": "Latitude",
                "stop_lon": "Longitude"
            }
        )
    )

    # -----------------------------
    # Transform Trips
    # -----------------------------

    trip_columns = [
        "route_id",
        "service_id",
        "trip_id",
        "trip_headsign",
        "direction_id"
    ]

    available_trip_columns = [
        column
        for column in trip_columns
        if column in trips_dataframe.columns
    ]

    cleaned_trips_dataframe = (
        trips_dataframe[
            available_trip_columns
        ].copy()
    )

    cleaned_trips_dataframe = (
        cleaned_trips_dataframe
        .drop_duplicates(
            subset=["trip_id"]
        )
    )

    cleaned_trips_dataframe = (
        cleaned_trips_dataframe.rename(
            columns={
                "route_id": "Route_ID",
                "service_id": "Service_ID",
                "trip_id": "Trip_ID",
                "trip_headsign": "Trip_Headsign",
                "direction_id": "Direction_ID"
            }
        )
    )

    # -----------------------------
    # Output Files
    # -----------------------------

    routes_output_file = (
        processed_folder
        / "nashville_transit_routes.csv"
    )

    stops_output_file = (
        processed_folder
        / "nashville_transit_stops.csv"
    )

    trips_output_file = (
        processed_folder
        / "nashville_transit_trips.csv"
    )

    # -----------------------------
    # Save Clean Data
    # -----------------------------

    cleaned_routes_dataframe.to_csv(
        routes_output_file,
        index=False
    )

    cleaned_stops_dataframe.to_csv(
        stops_output_file,
        index=False
    )

    cleaned_trips_dataframe.to_csv(
        trips_output_file,
        index=False
    )

    # -----------------------------
    # Display Results
    # -----------------------------

    print()
    print(
        "WeGo transit data transformed "
        "successfully."
    )

    print()

    print(
        f"Clean routes: "
        f"{len(cleaned_routes_dataframe)}"
    )

    print(
        f"Clean stops: "
        f"{len(cleaned_stops_dataframe)}"
    )

    print(
        f"Clean trips: "
        f"{len(cleaned_trips_dataframe)}"
    )

    print()

    print("Clean route columns:")
    print(
        cleaned_routes_dataframe.columns.tolist()
    )

    print()

    print("Clean stop columns:")
    print(
        cleaned_stops_dataframe.columns.tolist()
    )

    print()

    print("Clean trip columns:")
    print(
        cleaned_trips_dataframe.columns.tolist()
    )

    print()

    print("Sample routes:")
    print(
        cleaned_routes_dataframe.head()
    )

    print()

    print("Sample stops:")
    print(
        cleaned_stops_dataframe.head()
    )

    print()

    print("Sample trips:")
    print(
        cleaned_trips_dataframe.head()
    )

    print()

    print(
        f"Processed data saved to: "
        f"{processed_folder}"
    )


if __name__ == "__main__":
    transform_nashville_transit()