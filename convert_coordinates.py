import csv
import pathlib
import urllib.request
import logging
from pathlib import Path
from zipfile import ZipFile
from pyproj import Transformer
import pandas as pd

URL = "https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect"
POSTCODE_ARCHIVE_FILE_NAME = "codepo_gb.zip"
CSV_COLUMN_NAMES = [
    "Postcode",
    "Positional_quality_indicator",
    "Eastings",
    "Northings",
    "Country_code",
    "NHS_regional_HA_code",
    "NHS_HA_code",
    "Admin_county_code",
    "Admin_district_code",
    "Admin_ward_code"
]

logging.basicConfig(format="%(asctime)s:%(levelname)s: %(message)s", level=logging.INFO)

transform = Transformer.from_crs('EPSG:27700', 'EPSG:4326')


def download_postcode_data(filepath: Path) -> None:
    """
    Download the postcode file ordinance survey
    :param filepath: where we want to place the downloaded file
    :return: None
    """
    logging.debug("download CSV files")

    urllib.request.urlretrieve(URL, filepath)


def coords_from_uk_easting_northing(easting, northing) -> tuple[float, float]:
    """
    converts the easting and northing from ESPG:27700 coordinates to WSG84 coords
    :param easting: the ESPG:27700 coordinate
    :param northing: the ESPG:27700 coordinate
    :return: Tuple(float, float) representing the lat,lng
    """
    lng, lat = transform.transform(easting, northing)

    return lat, lng


def process_csv_files(input_path: Path, output_path: Path) -> None:
    """
    This just looks through all the postcode CSV files in the archive and then converts them
    :param input_path: the extracted path of our code point open archive
    :param output_path: the output path of the converted files
    :return: None
    """
    csv_path = input_path.joinpath("Data/CSV")

    if not csv_path.exists():
        logging.info("could not find the Data/CSV directory")

    postcode_csvs = csv_path.glob("*.csv")

    for input_file in postcode_csvs:
        if input_file.is_dir():
            continue

        logging.info(f"converting csv file: {input_file.name}")

        records = []

        df = pd.read_csv(input_file, header=None, index_col=False, names=CSV_COLUMN_NAMES)

        for index, row in df.iterrows():
            postcode = row["Postcode"]  # POSTCODE is always on the first column
            eastings = row["Eastings"]  # EASTING is always on the third column
            northings = row["Northings"]  # NORTHING is always on the fourth col

            lng, lat = coords_from_uk_easting_northing(eastings, northings)

            record = {
                "postcode": postcode,
                "lat": lat,
                "lng": lng
            }

            logging.debug(f"processing: {record}")

            records.append(record)

        output_file = output_path.joinpath(input_file.name)

        with open(output_file, mode="w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, ["postcode", "lat", "lng"])
            writer.writerows(records)


def main():
    # setup directory to download geolocation data into
    logging.info("starting postcode location conversion")
    input_path = pathlib.Path.cwd().joinpath("input")
    input_path.mkdir(exist_ok=True)

    # get the archive file path
    archive_file = input_path.joinpath(POSTCODE_ARCHIVE_FILE_NAME)

    if not archive_file.exists():
        logging.info(f"downloading postcode data from: {URL}")
        # get hold of the postcode data
        download_postcode_data(archive_file)

    # get the output path and create it if exists
    output_path = Path.cwd().joinpath("output")
    output_path.mkdir(exist_ok=True)

    # extract the archive
    logging.info(f"extracting postcode archive: {archive_file}")
    with ZipFile(archive_file) as zObject:
        zObject.extractall(path=input_path)

    # process the CSV files
    process_csv_files(input_path, output_path)


if __name__ == "__main__":
    main()
