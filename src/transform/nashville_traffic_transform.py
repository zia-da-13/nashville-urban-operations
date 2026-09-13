import pandas as pd
from pathlib import Path


def transform_nashville_traffic():
    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_traffic_raw.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "nashville_traffic_clean.csv"
    )

    dataframe = pd.read_csv(input_file)

    print("Original traffic data:")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    print()

    # -----------------------------
    # Remove Duplicate Records
    # -----------------------------

    dataframe = dataframe.drop_duplicates(
        subset=["OBJECTID"]
    )


    # -----------------------------
    # Convert Crash Date
    # -----------------------------

    numeric_dates = pd.to_numeric(
        dataframe["DATEOFCRAS"],
        errors="coerce"
    )

    dataframe["Crash_Date"] = pd.to_datetime(
        numeric_dates,
        unit="ms",
        errors="coerce"
    )


    # -----------------------------
    # Convert Numeric Columns
    # -----------------------------

    numeric_columns = [
        "YEAROFCRAS",
        "TOTALKILLE",
        "TOTALINJUR",
        "TOTALVEHIC",
        "Longitude",
        "Latitude"
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )


    # -----------------------------
    # Select Important Columns
    # -----------------------------

    cleaned_dataframe = dataframe[
        [
            "OBJECTID",
            "ID_NUMBER",
            "CASENO",
            "NBR_TENN_C",
            "YEAROFCRAS",
            "Crash_Date",
            "TIMEOFCRAS",
            "TYPEOFCRAS",
            "TOTALKILLE",
            "TOTALINJUR",
            "TOTALVEHIC",
            "FIRSTHARMF",
            "MANNEROFCO",
            "WEATHERCON",
            "LIGHTCONDI",
            "LOCATE_TYP",
            "Longitude",
            "Latitude"
        ]
    ].copy()


    # -----------------------------
    # Rename Columns
    # -----------------------------

    cleaned_dataframe = cleaned_dataframe.rename(
        columns={
            "OBJECTID": "Object_ID",
            "ID_NUMBER": "Crash_ID",
            "CASENO": "Case_Number",
            "NBR_TENN_C": "County",
            "YEAROFCRAS": "Crash_Year",
            "TIMEOFCRAS": "Crash_Time",
            "TYPEOFCRAS": "Crash_Type",
            "TOTALKILLE": "Fatalities",
            "TOTALINJUR": "Injuries",
            "TOTALVEHIC": "Vehicles_Involved",
            "FIRSTHARMF": "First_Harmful_Event",
            "MANNEROFCO": "Collision_Manner",
            "WEATHERCON": "Weather_Condition",
            "LIGHTCONDI": "Light_Condition",
            "LOCATE_TYP": "Location_Type"
        }
    )


    # -----------------------------
    # Save Cleaned Data
    # -----------------------------

    cleaned_dataframe.to_csv(
        output_file,
        index=False
    )


    # -----------------------------
    # Results
    # -----------------------------

    print("Nashville traffic data transformed successfully.")
    print()

    print(
        f"Rows after transformation: "
        f"{len(cleaned_dataframe)}"
    )

    print(
        f"Columns after transformation: "
        f"{len(cleaned_dataframe.columns)}"
    )

    print()
    print("Cleaned columns:")
    print(cleaned_dataframe.columns.tolist())

    print()
    print(cleaned_dataframe.head())

    print()
    print(
        f"Clean data saved to: {output_file}"
    )


if __name__ == "__main__":
    transform_nashville_traffic()