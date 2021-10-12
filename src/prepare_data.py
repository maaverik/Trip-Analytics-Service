import os
import gdown
import logging
import sys
from .trip_analysis import TaxiTripAnalyser

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def download_dataset_from_drive(url, output_path):
    """Download the dataset from google drive and save it to output path."""
    logger.info("Downloading dataset from google drive...")
    parent_folder = os.path.dirname(output_path)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    gdown.download(url, output_path, quiet=False)


if __name__ == "__main__":
    url = "https://drive.google.com/u/0/uc?id=1QLBGFOoKw_3-iM58q4unWfwHmPqfnrYr&export=download"
    output_path = r"data/chicago_taxi_trips_2020.parquet"
    download_dataset_from_drive(url, output_path)

    TaxiTripAnalyser.load_from_unprocessed_parquet(output_path)
