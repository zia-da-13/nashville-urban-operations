import pandas as pd
from pathlib import Path
from sqlalchemy import text

from src.database.database_connection import get_database_engine


def load_nashville_traffic():
    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "processed"
        / "nashville_traffic_clean.csv"
    )

    dataframe = pd.read_csv(input_file)

    engine = get_database_engine()

    table_name = "nashville_traffic"

    dataframe.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(
        "Nashville traffic data loaded into the database."
    )

    print(
        f"Rows loaded: {len(dataframe)}"
    )

    with engine.connect() as connection:
        result = connection.execute(
            text(
                "SELECT COUNT(*) "
                "FROM nashville_traffic"
            )
        )

        database_row_count = result.scalar()

    print(
        f"Rows verified in database: "
        f"{database_row_count}"
    )


if __name__ == "__main__":
    load_nashville_traffic()