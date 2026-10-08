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
    # Convert Date and Time
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
    # Convert Temperature
    # -----------------------------

    dataframe["Temperature"] = pd.to_numeric(
        dataframe["Temperature"],
        errors="coerce"
    )

    # -----------------------------
    # Convert Precipitation
    # -----------------------------

    dataframe["Precipitation_Probability"] = (
        pd.to_numeric(
            dataframe["Precipitation_Probability"],
            errors="coerce"
        )
    )

    # -----------------------------
    # Clean Wind Speed
    # -----------------------------

    dataframe["Wind_Speed_MPH"] = (
        dataframe["Wind_Speed"]
        .astype("string")
        .str.extract(r"(\d+)", expand=False)
    )

    dataframe["Wind_Speed_MPH"] = pd.to_numeric(
        dataframe["Wind_Speed_MPH"],
        errors="coerce"
    )

    # -----------------------------
    # Convert Map Coordinates
    # -----------------------------

    dataframe["Latitude"] = pd.to_numeric(
        dataframe["Latitude"],
        errors="coerce"
    )

    dataframe["Longitude"] = pd.to_numeric(
        dataframe["Longitude"],
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
            "Short_Forecast",
            "Latitude",
            "Longitude"
        ]
    ].copy()

    # -----------------------------
    # Remove Duplicate Forecasts
    # -----------------------------

    cleaned_dataframe = (
        cleaned_dataframe.drop_duplicates(
            subset=[
                "Forecast_Number",
                "Start_Time"
            ]
        )
    )

    # -----------------------------
    # Sort Forecast
    # -----------------------------

    cleaned_dataframe = (
        cleaned_dataframe.sort_values(
            by="Start_Time"
        )
    )

    # -----------------------------
    # Save Clean Data
    # -----------------------------

    cleaned_dataframe.to_csv(
        output_file,
        index=False
    )

    # -----------------------------
    # Display Results
    # -----------------------------

    print(
        "Nashville weather data "
        "transformed successfully."
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