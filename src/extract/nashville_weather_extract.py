import requests
import pandas as pd
from pathlib import Path


POINTS_URL = (
    "https://api.weather.gov/points/"
    "36.1627,-86.7816"
)

HEADERS = {
    "User-Agent": (
        "NashvilleUrbanOperationsProject "
        "student-data-engineering-project"
    )
}


def get_forecast_url():
    response = requests.get(
        POINTS_URL,
        headers=HEADERS,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    forecast_url = (
        data["properties"]["forecastHourly"]
    )

    return forecast_url


def extract_nashville_weather():
    print(
        "Downloading Nashville hourly weather forecast..."
    )

    forecast_url = get_forecast_url()

    response = requests.get(
        forecast_url,
        headers=HEADERS,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    periods = data["properties"]["periods"]

    records = []

    for period in periods:

        record = {
            "Forecast_Number": period.get(
                "number"
            ),
            "Start_Time": period.get(
                "startTime"
            ),
            "End_Time": period.get(
                "endTime"
            ),
            "Temperature": period.get(
                "temperature"
            ),
            "Temperature_Unit": period.get(
                "temperatureUnit"
            ),
            "Precipitation_Probability": (
                period.get(
                    "probabilityOfPrecipitation",
                    {}
                ).get("value")
            ),
            "Wind_Speed": period.get(
                "windSpeed"
            ),
            "Wind_Direction": period.get(
                "windDirection"
            ),
            "Short_Forecast": period.get(
                "shortForecast"
            )
        }

        records.append(record)

    dataframe = pd.DataFrame(records)

    return dataframe


def save_raw_data(dataframe):
    project_root = Path(__file__).resolve().parents[2]

    output_file = (
        project_root
        / "data"
        / "raw"
        / "nashville_weather_raw.csv"
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
    nashville_weather_data = (
        extract_nashville_weather()
    )

    print()
    print(
        "Nashville weather extraction completed."
    )

    print(
        f"Total rows extracted: "
        f"{len(nashville_weather_data)}"
    )

    print()
    print("Columns:")

    print(
        nashville_weather_data.columns.tolist()
    )

    print()

    print(
        nashville_weather_data.head()
    )

    save_raw_data(
        nashville_weather_data
    )