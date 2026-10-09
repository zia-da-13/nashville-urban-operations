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

    stop_times_file = (
        raw_folder
        / "stop_times.txt"
    )

    shapes_file = (
        raw_folder
        / "shapes.txt"
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

    stop_times_dataframe = pd.read_csv(
        stop_times_file,
        dtype=str
    )

    shapes_dataframe = pd.read_csv(
        shapes_file,
        dtype=str
    )

    print()
    print(
        f"Routes loaded: "
        f"{len(routes_dataframe):,}"
    )

    print(
        f"Stops loaded: "
        f"{len(stops_dataframe):,}"
    )

    print(
        f"Trips loaded: "
        f"{len(trips_dataframe):,}"
    )

    print(
        f"Stop times loaded: "
        f"{len(stop_times_dataframe):,}"
    )

    print(
        f"Shape points loaded: "
        f"{len(shapes_dataframe):,}"
    )

    # -----------------------------
    # Transform Routes
    # -----------------------------

    cleaned_routes_dataframe = (
        routes_dataframe[
            [
                "route_id",
                "route_short_name",
                "route_long_name",
                "route_type"
            ]
        ]
        .copy()
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

    cleaned_stops_dataframe = (
        stops_dataframe[
            [
                "stop_id",
                "stop_name",
                "stop_lat",
                "stop_lon"
            ]
        ]
        .copy()
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

    if "shape_id" in trips_dataframe.columns:
        trip_columns.append(
            "shape_id"
        )

    cleaned_trips_dataframe = (
        trips_dataframe[
            trip_columns
        ]
        .copy()
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
                "direction_id": "Direction_ID",
                "shape_id": "Shape_ID"
            }
        )
    )

    # -----------------------------
    # Transform Stop Times
    # -----------------------------

    cleaned_stop_times_dataframe = (
        stop_times_dataframe[
            [
                "trip_id",
                "arrival_time",
                "departure_time",
                "stop_id",
                "stop_sequence"
            ]
        ]
        .copy()
    )

    cleaned_stop_times_dataframe[
        "stop_sequence"
    ] = pd.to_numeric(
        cleaned_stop_times_dataframe[
            "stop_sequence"
        ],
        errors="coerce"
    )

    cleaned_stop_times_dataframe = (
        cleaned_stop_times_dataframe.rename(
            columns={
                "trip_id": "Trip_ID",
                "arrival_time": "Arrival_Time",
                "departure_time": "Departure_Time",
                "stop_id": "Stop_ID",
                "stop_sequence": "Stop_Sequence"
            }
        )
    )

    cleaned_stop_times_dataframe = (
        cleaned_stop_times_dataframe
        .sort_values(
            by=[
                "Trip_ID",
                "Stop_Sequence"
            ]
        )
    )

    # -----------------------------
    # Transform Shapes
    # -----------------------------

    cleaned_shapes_dataframe = (
        shapes_dataframe[
            [
                "shape_id",
                "shape_pt_lat",
                "shape_pt_lon",
                "shape_pt_sequence",
                "shape_dist_traveled"
            ]
        ]
        .copy()
    )

    cleaned_shapes_dataframe[
        "shape_pt_lat"
    ] = pd.to_numeric(
        cleaned_shapes_dataframe[
            "shape_pt_lat"
        ],
        errors="coerce"
    )

    cleaned_shapes_dataframe[
        "shape_pt_lon"
    ] = pd.to_numeric(
        cleaned_shapes_dataframe[
            "shape_pt_lon"
        ],
        errors="coerce"
    )

    cleaned_shapes_dataframe[
        "shape_pt_sequence"
    ] = pd.to_numeric(
        cleaned_shapes_dataframe[
            "shape_pt_sequence"
        ],
        errors="coerce"
    )

    cleaned_shapes_dataframe[
        "shape_dist_traveled"
    ] = pd.to_numeric(
        cleaned_shapes_dataframe[
            "shape_dist_traveled"
        ],
        errors="coerce"
    )

    cleaned_shapes_dataframe = (
        cleaned_shapes_dataframe.rename(
            columns={
                "shape_id": "Shape_ID",
                "shape_pt_lat": "Latitude",
                "shape_pt_lon": "Longitude",
                "shape_pt_sequence": "Shape_Point_Sequence",
                "shape_dist_traveled": "Shape_Distance_Traveled"
            }
        )
    )

    cleaned_shapes_dataframe = (
        cleaned_shapes_dataframe
        .dropna(
            subset=[
                "Latitude",
                "Longitude"
            ]
        )
    )

    cleaned_shapes_dataframe = (
        cleaned_shapes_dataframe
        .sort_values(
            by=[
                "Shape_ID",
                "Shape_Point_Sequence"
            ]
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

    stop_times_output_file = (
        processed_folder
        / "nashville_transit_stop_times.csv"
    )

    shapes_output_file = (
        processed_folder
        / "nashville_transit_shapes.csv"
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

    cleaned_stop_times_dataframe.to_csv(
        stop_times_output_file,
        index=False
    )

    cleaned_shapes_dataframe.to_csv(
        shapes_output_file,
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
        f"{len(cleaned_routes_dataframe):,}"
    )

    print(
        f"Clean stops: "
        f"{len(cleaned_stops_dataframe):,}"
    )

    print(
        f"Clean trips: "
        f"{len(cleaned_trips_dataframe):,}"
    )

    print(
        f"Clean stop times: "
        f"{len(cleaned_stop_times_dataframe):,}"
    )

    print(
        f"Clean shape points: "
        f"{len(cleaned_shapes_dataframe):,}"
    )

    print()

    print("Clean trip columns:")
    print(
        cleaned_trips_dataframe.columns.tolist()
    )

    print()

    print("Clean stop time columns:")
    print(
        cleaned_stop_times_dataframe.columns.tolist()
    )

    print()

    print("Clean shape columns:")
    print(
        cleaned_shapes_dataframe.columns.tolist()
    )

    print()

    print("Sample stop times:")
    print(
        cleaned_stop_times_dataframe.head()
    )

    print()

    print("Sample shape points:")
    print(
        cleaned_shapes_dataframe.head()
    )

    print()

    print(
        f"Processed data saved to: "
        f"{processed_folder}"
    )


if __name__ == "__main__":
    transform_nashville_transit()