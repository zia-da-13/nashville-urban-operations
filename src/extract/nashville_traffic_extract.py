import requests
import pandas as pd
from pathlib import Path


API_URL = (
    "https://services2.arcgis.com/"
    "nf3p7v7Zy4fTOh6M/"
    "ArcGIS/rest/services/"
    "Tennessee_Crashes_JAN_2021_JAN_2025/"
    "FeatureServer/0/query"
)


def extract_nashville_traffic():
    parameters = {
        "where": "NBR_TENN_C = 'DAVIDSON'",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "resultRecordCount": 2000,
        "orderByFields": "DATEOFCRAS DESC",
        "f": "json"
    }

    print(
        "Downloading Davidson County "
        "traffic accident records..."
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
            "The API response was not valid JSON."
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
        / "nashville_traffic_raw.csv"
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
    nashville_traffic_data = (
        extract_nashville_traffic()
    )

    print()
    print(
        "Nashville traffic extraction completed."
    )

    print(
        f"Total rows extracted: "
        f"{len(nashville_traffic_data)}"
    )

    print()
    print("Columns:")

    print(
        nashville_traffic_data.columns.tolist()
    )

    print()
    print(
        nashville_traffic_data.head()
    )

    save_raw_data(
        nashville_traffic_data
    )