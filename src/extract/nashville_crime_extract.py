import requests
import pandas as pd
from pathlib import Path


API_URL = (
    "https://services2.arcgis.com/"
    "HdTo6HJqh92wn4D8/"
    "ArcGIS/rest/services/"
    "Metro_Nashville_Police_Department_Incidents_view/"
    "FeatureServer/0/query"
)


def extract_nashville_crime():
    parameters = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": 2000,
        "orderByFields": "Incident_Reported DESC",
        "f": "json"
    }

    print(
        "Downloading Nashville police incident records..."
    )

    response = requests.get(
        API_URL,
        params=parameters,
        timeout=120
    )

    response.raise_for_status()

    try:
        data = response.json()

    except requests.exceptions.JSONDecodeError:

        raise RuntimeError(
            "The Nashville police API response "
            "was not valid JSON."
        )

    if "error" in data:

        raise RuntimeError(
            f"ArcGIS API error: {data['error']}"
        )

    records = []

    for feature in data.get("features", []):

        attributes = feature.get(
            "attributes",
            {}
        )

        geometry = feature.get(
            "geometry",
            {}
        )

        attributes["Longitude"] = geometry.get("x")
        attributes["Latitude"] = geometry.get("y")

        records.append(attributes)

    dataframe = pd.DataFrame(records)

    return dataframe


def save_raw_data(dataframe):
    project_root = Path(__file__).resolve().parents[2]

    output_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_crime_raw.csv"
    )

    dataframe.to_csv(
        output_file,
        index=False
    )

    print()

    print(
        f"Data saved to: {output_file}"
    )


if __name__ == "__main__":
    nashville_crime_data = (
        extract_nashville_crime()
    )

    print()

    print(
        "Nashville police incident extraction completed."
    )

    print(
        f"Total rows extracted: "
        f"{len(nashville_crime_data)}"
    )

    print()

    print("Columns:")

    print(
        nashville_crime_data.columns.tolist()
    )

    print()

    print(
        nashville_crime_data.head()
    )

    save_raw_data(
        nashville_crime_data
    )