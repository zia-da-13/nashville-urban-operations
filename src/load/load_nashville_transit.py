import pandas as pd
from pathlib import Path
from sqlalchemy import text

from src.database.database_connection import get_database_engine


def load_nashville_transit():
    project_root = Path(__file__).resolve().parents[2]

    processed_folder = (
        project_root
        / "data"
        / "processed"
        / "nashville_transit"
    )

    routes_file = (
        processed_folder
        / "nashville_transit_routes.csv"
    )

    stops_file = (
        processed_folder
        / "nashville_transit_stops.csv"
    )

    trips_file = (
        processed_folder
        / "nashville_transit_trips.csv"
    )

    stop_times_file = (
        processed_folder
        / "nashville_transit_stop_times.csv"
    )

    shapes_file = (
        processed_folder
        / "nashville_transit_shapes.csv"
    )

    # -----------------------------
    # Read Processed Data
    # -----------------------------

    print(
        "Reading processed WeGo transit data..."
    )

    routes_dataframe = pd.read_csv(
        routes_file
    )

    stops_dataframe = pd.read_csv(
        stops_file
    )

    trips_dataframe = pd.read_csv(
        trips_file
    )

    stop_times_dataframe = pd.read_csv(
        stop_times_file
    )

    shapes_dataframe = pd.read_csv(
        shapes_file
    )

    # -----------------------------
    # Database Connection
    # -----------------------------

    engine = get_database_engine()

    # -----------------------------
    # Load Routes
    # -----------------------------

    routes_dataframe.to_sql(
        "nashville_transit_routes",
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit routes loaded into database."
    )

    print(
        f"Rows loaded: {len(routes_dataframe):,}"
    )

    # -----------------------------
    # Load Stops
    # -----------------------------

    stops_dataframe.to_sql(
        "nashville_transit_stops",
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit stops loaded into database."
    )

    print(
        f"Rows loaded: {len(stops_dataframe):,}"
    )

    # -----------------------------
    # Load Trips
    # -----------------------------

    trips_dataframe.to_sql(
        "nashville_transit_trips",
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit trips loaded into database."
    )

    print(
        f"Rows loaded: {len(trips_dataframe):,}"
    )

    # -----------------------------
    # Load Stop Times
    # -----------------------------

    stop_times_dataframe.to_sql(
        "nashville_transit_stop_times",
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit stop times loaded into database."
    )

    print(
        f"Rows loaded: "
        f"{len(stop_times_dataframe):,}"
    )

    # -----------------------------
    # Load Shapes
    # -----------------------------

    shapes_dataframe.to_sql(
        "nashville_transit_shapes",
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit route shapes loaded into database."
    )

    print(
        f"Rows loaded: "
        f"{len(shapes_dataframe):,}"
    )

    # -----------------------------
    # Verify Database Tables
    # -----------------------------

    table_names = [
        "nashville_transit_routes",
        "nashville_transit_stops",
        "nashville_transit_trips",
        "nashville_transit_stop_times",
        "nashville_transit_shapes"
    ]

    print()
    print(
        "Database verification:"
    )

    with engine.connect() as connection:

        for table_name in table_names:

            result = connection.execute(
                text(
                    f"SELECT COUNT(*) "
                    f"FROM {table_name}"
                )
            )

            row_count = result.scalar()

            print(
                f"{table_name}: "
                f"{row_count:,} rows"
            )

    print()
    print(
        "WeGo transit database load completed."
    )


if __name__ == "__main__":
    load_nashville_transit()