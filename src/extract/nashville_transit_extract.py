import requests
import zipfile
from io import BytesIO
from pathlib import Path


GTFS_URL = (
    "https://www.wegotransit.com/"
    "GoogleExport/google_transit.zip"
)


def extract_nashville_transit():
    project_root = Path(__file__).resolve().parents[2]

    output_folder = (
        project_root
        / "data"
        / "raw"
        / "nashville_transit"
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "Downloading WeGo Nashville GTFS data..."
    )

    response = requests.get(
        GTFS_URL,
        timeout=120
    )

    response.raise_for_status()

    print(
        "Download completed successfully."
    )

    # -----------------------------
    # Open GTFS ZIP File
    # -----------------------------

    with zipfile.ZipFile(
        BytesIO(response.content)
    ) as zip_file:

        file_names = zip_file.namelist()

        print()
        print("Files available in GTFS feed:")

        for file_name in file_names:
            print(file_name)

        # -----------------------------
        # Important GTFS Files
        # -----------------------------

        important_files = [
            "agency.txt",
            "routes.txt",
            "stops.txt",
            "trips.txt",
            "stop_times.txt",
            "shapes.txt",
            "calendar.txt",
            "calendar_dates.txt"
        ]

        print()
        print(
            "Extracting important GTFS files..."
        )

        extracted_files = []

        for file_name in important_files:

            if file_name in file_names:

                zip_file.extract(
                    file_name,
                    output_folder
                )

                extracted_files.append(
                    file_name
                )

                print(
                    f"Extracted: {file_name}"
                )

            else:

                print(
                    f"Not available: {file_name}"
                )

    # -----------------------------
    # Summary
    # -----------------------------

    print()
    print(
        "Nashville transit extraction completed."
    )

    print(
        f"Files extracted: "
        f"{len(extracted_files)}"
    )

    print()

    print(
        f"Data saved to: {output_folder}"
    )


if __name__ == "__main__":
    extract_nashville_transit()