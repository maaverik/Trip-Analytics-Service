import os
import gdown
from src.trip_analysis import TaxiTripAnalyser
from src.utils import get_default_logger

logger = get_default_logger(__name__)


def download_dataset_from_drive(url, output_path):
    """Download the dataset from google drive and save it to output path."""
    logger.info("Downloading dataset from google drive...")
    parent_folder = os.path.dirname(output_path)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    gdown.download(url, output_path, quiet=False)


def download_and_preprocess_data(url, output_path):
    download_dataset_from_drive(url, output_path)
    TaxiTripAnalyser.load_and_process_unprocessed_parquet(output_path)


if __name__ == "__main__":
    url = "https://drive.google.com/u/0/uc?id=1QLBGFOoKw_3-iM58q4unWfwHmPqfnrYr&export=download"
    output_path = r"data/chicago_taxi_trips_2020.parquet"
    download_and_preprocess_data(url, output_path)
