import pandas as pd
from pathlib import Path


def transform_nashville_weather():
    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_weather_raw.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "nashville_weather_clean.csv"
    )

    dataframe = pd.read_csv(input_file)

    print("Original weather data:")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    print()

    # -----------------------------
    # Remove Duplicate Records
    # -----------------------------

    dataframe = dataframe.drop_duplicates(
        subset=["Forecast_Number"]
    )

    # -----------------------------
    # Convert Date and Time Fields
    # -----------------------------

    dataframe["Start_Time"] = pd.to_datetime(
        dataframe["Start_Time"],
        errors="coerce"
    )

    dataframe["End_Time"] = pd.to_datetime(
        dataframe["End_Time"],
        errors="coerce"
    )

    # -----------------------------
    # Convert Numeric Fields
    # -----------------------------

    numeric_columns = [
        "Forecast_Number",
        "Temperature",
        "Precipitation_Probability"
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    # -----------------------------
    # Extract Wind Speed Number
    # -----------------------------

    dataframe["Wind_Speed_MPH"] = (
        dataframe["Wind_Speed"]
        .astype("string")
        .str.extract(r"(\d+)")
        [0]
    )

    dataframe["Wind_Speed_MPH"] = pd.to_numeric(
        dataframe["Wind_Speed_MPH"],
        errors="coerce"
    )

    # -----------------------------
    # Select Clean Columns
    # -----------------------------

    cleaned_dataframe = dataframe[
        [
            "Forecast_Number",
            "Start_Time",
            "End_Time",
            "Temperature",
            "Temperature_Unit",
            "Precipitation_Probability",
            "Wind_Speed_MPH",
            "Wind_Direction",
            "Short_Forecast"
        ]
    ].copy()

    # -----------------------------
    # Save Cleaned Data
    # -----------------------------

    cleaned_dataframe.to_csv(
        output_file,
        index=False
    )

    # -----------------------------
    # Display Results
    # -----------------------------

    print(
        "Nashville weather data transformed successfully."
    )

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
    print(
        cleaned_dataframe.columns.tolist()
    )

    print()

    print(
        cleaned_dataframe.head()
    )

    print()

    print(
        f"Clean data saved to: {output_file}"
    )


if __name__ == "__main__":
    transform_nashville_weather()