import pandas as pd
from pathlib import Path


def transform_nashville_crime():
    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_crime_raw.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "nashville_crime_clean.csv"
    )

    dataframe = pd.read_csv(input_file)

    print("Original crime data:")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    print()

    # -----------------------------
    # Remove Duplicate Records
    # -----------------------------

    dataframe = dataframe.drop_duplicates(
        subset=["Primary_Key"]
    )

    # -----------------------------
    # Convert Incident Dates
    # -----------------------------

    occurred_dates = pd.to_numeric(
        dataframe["Incident_Occurred"],
        errors="coerce"
    )

    dataframe["Incident_Occurred"] = pd.to_datetime(
        occurred_dates,
        unit="ms",
        errors="coerce"
    )

    reported_dates = pd.to_numeric(
        dataframe["Incident_Reported"],
        errors="coerce"
    )

    dataframe["Incident_Reported"] = pd.to_datetime(
        reported_dates,
        unit="ms",
        errors="coerce"
    )

    # -----------------------------
    # Clean ZIP Code
    # -----------------------------

    dataframe["ZIP_Code"] = (
        pd.to_numeric(
            dataframe["ZIP_Code"],
            errors="coerce"
        )
        .astype("Int64")
        .astype("string")
    )

    # -----------------------------
    # Convert Coordinates
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
    # Select Important Columns
    # -----------------------------

    cleaned_dataframe = dataframe[
        [
            "Primary_Key",
            "Incident_Number",
            "Report_Type_Description",
            "Incident_Status_Description",
            "Investigation_Status",
            "Incident_Location",
            "Location_Description",
            "Offense_NIBRS",
            "Offense_Description",
            "Weapon_Description",
            "Domestic_Related",
            "Victim_Type",
            "Victim_Description",
            "Victim_Gender",
            "Victim_Race",
            "Victim_Ethnicity",
            "ZIP_Code",
            "Incident_Occurred",
            "Incident_Reported",
            "Latitude",
            "Longitude"
        ]
    ].copy()

    # -----------------------------
    # Rename Columns
    # -----------------------------

    cleaned_dataframe = cleaned_dataframe.rename(
        columns={
            "Primary_Key": "Primary_Key",
            "Incident_Number": "Incident_Number",
            "Report_Type_Description": "Report_Type",
            "Incident_Status_Description": "Incident_Status",
            "Investigation_Status": "Investigation_Status",
            "Incident_Location": "Incident_Location",
            "Location_Description": "Location_Type",
            "Offense_NIBRS": "NIBRS_Code",
            "Offense_Description": "Offense_Description",
            "Weapon_Description": "Weapon_Description",
            "Domestic_Related": "Domestic_Related",
            "Victim_Type": "Victim_Type",
            "Victim_Description": "Victim_Description",
            "Victim_Gender": "Victim_Gender",
            "Victim_Race": "Victim_Race",
            "Victim_Ethnicity": "Victim_Ethnicity",
            "ZIP_Code": "ZIP_Code",
            "Incident_Occurred": "Incident_Occurred",
            "Incident_Reported": "Incident_Reported",
            "Latitude": "Latitude",
            "Longitude": "Longitude"
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
    # Display Results
    # -----------------------------

    print(
        "Nashville crime data transformed successfully."
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
    transform_nashville_crime()