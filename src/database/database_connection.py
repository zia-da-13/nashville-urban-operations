from pathlib import Path
from sqlalchemy import create_engine


def get_database_engine():
    project_root = Path(__file__).resolve().parents[2]

    database_file = (
        project_root
        / "data"
        / "output"
        / "nashville_urban_operations.db"
    )

    database_url = f"sqlite:///{database_file}"

    engine = create_engine(database_url)

    return engine


if __name__ == "__main__":
    engine = get_database_engine()

    connection = engine.connect()

    print("Database connection successful.")

    connection.close()