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

    # -----------------------------
    # Database Connection
    # -----------------------------

    engine = get_database_engine()

    # -----------------------------
    # Load Routes
    # -----------------------------

    routes_table = (
        "nashville_transit_routes"
    )

    routes_dataframe.to_sql(
        routes_table,
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit routes loaded into database."
    )

    print(
        f"Rows loaded: {len(routes_dataframe)}"
    )

    # -----------------------------
    # Load Stops
    # -----------------------------

    stops_table = (
        "nashville_transit_stops"
    )

    stops_dataframe.to_sql(
        stops_table,
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit stops loaded into database."
    )

    print(
        f"Rows loaded: {len(stops_dataframe)}"
    )

    # -----------------------------
    # Load Trips
    # -----------------------------

    trips_table = (
        "nashville_transit_trips"
    )

    trips_dataframe.to_sql(
        trips_table,
        engine,
        if_exists="replace",
        index=False
    )

    print()
    print(
        "Transit trips loaded into database."
    )

    print(
        f"Rows loaded: {len(trips_dataframe)}"
    )

    # -----------------------------
    # Verify Database Tables
    # -----------------------------

    with engine.connect() as connection:

        routes_result = connection.execute(
            text(
                "SELECT COUNT(*) "
                "FROM nashville_transit_routes"
            )
        )

        routes_count = (
            routes_result.scalar()
        )

        stops_result = connection.execute(
            text(
                "SELECT COUNT(*) "
                "FROM nashville_transit_stops"
            )
        )

        stops_count = (
            stops_result.scalar()
        )

        trips_result = connection.execute(
            text(
                "SELECT COUNT(*) "
                "FROM nashville_transit_trips"
            )
        )

        trips_count = (
            trips_result.scalar()
        )

    # -----------------------------
    # Display Verification
    # -----------------------------

    print()
    print(
        "Database verification completed."
    )

    print(
        f"Routes verified: {routes_count}"
    )

    print(
        f"Stops verified: {stops_count}"
    )

    print(
        f"Trips verified: {trips_count}"
    )


if __name__ == "__main__":
    load_nashville_transit()