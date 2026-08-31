import pandas as pd
from pathlib import Path


def transform_nashville_311():
    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_311_raw.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "nashville_311_clean.csv"
    )

    dataframe = pd.read_csv(input_file)

    print("Original columns:")
    print(dataframe.columns.tolist())
    print()

    # Convert ArcGIS timestamps from milliseconds
    dataframe["Date_Time_Opened"] = pd.to_datetime(
        dataframe["Date_Time_Opened"],
        unit="ms",
        errors="coerce"
    )

    dataframe["Date_Time_Closed"] = pd.to_datetime(
        dataframe["Date_Time_Closed"],
        unit="ms",
        errors="coerce"
    )

    # Remove duplicate records
    dataframe = dataframe.drop_duplicates(
        subset=["OBJECTID"]
    )

    # Clean ZIP codes
    dataframe["ZIP"] = (
    pd.to_numeric(dataframe["ZIP"], errors="coerce")
    .astype("Int64")
    .astype("string")
)

    # Save cleaned dataset
    dataframe.to_csv(
        output_file,
        index=False
    )

    print("Nashville 311 data transformed successfully.")
    print()
    print(dataframe.head())
    print()
    print(f"Rows after transformation: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    print()
    print(f"Clean data saved to: {output_file}")


if __name__ == "__main__":
    transform_nashville_311()