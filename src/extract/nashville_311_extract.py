import requests
import pandas as pd
from pathlib import Path


API_URL = (
    "https://services2.arcgis.com/HdTo6HJqh92wn4D8/"
    "arcgis/rest/services/"
    "hubNashville_(311)_Service_Requests_1/"
    "FeatureServer/0/query"
)


def extract_nashville_311():
    parameters = {
        "where": "1=1",
        "outFields": "*",
        "f": "json",
        "resultRecordCount": 10000,
        "orderByFields": "OBJECTID DESC"
    }

    print("Downloading recent Nashville 311 records...")

    response = requests.get(
        API_URL,
        params=parameters,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(
            f"ArcGIS API error: {data['error']}"
        )

    records = [
        feature["attributes"]
        for feature in data.get("features", [])
    ]

    dataframe = pd.DataFrame(records)

    return dataframe


def save_raw_data(dataframe):
    project_root = Path(__file__).resolve().parents[2]

    output_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_311_raw.csv"
    )

    dataframe.to_csv(
        output_file,
        index=False
    )

    print(f"Data saved to: {output_file}")


if __name__ == "__main__":
    nashville_311_data = extract_nashville_311()

    print()
    print("Nashville 311 extraction completed.")
    print(f"Total rows extracted: {len(nashville_311_data)}")
    print()

    save_raw_data(nashville_311_data)