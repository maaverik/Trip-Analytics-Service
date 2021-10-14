import os
import gdown
from src.trip_analysis import TaxiTripAnalyser
from src.utils import get_default_logger, get_config

logger = get_default_logger(__name__)


def download_dataset_from_drive(url, output_path):
    """Download the dataset from google drive and save it to output path."""
    logger.info("Downloading dataset from google drive...")
    parent_folder = os.path.dirname(output_path)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    gdown.download(url, output_path, quiet=False)


def download_and_preprocess_data(url, unprocessed_data_path, processed_data_path):
    download_dataset_from_drive(url, unprocessed_data_path)
    analyser = TaxiTripAnalyser.load_and_process_unprocessed_parquet(
        unprocessed_data_path
    )
    analyser.store_df_as_csv(processed_data_path)


if __name__ == "__main__":
    config = get_config()
    url = config["dataset_download_url"]
    unprocessed_data_path = config["unprocessed_data_path"]
    processed_data_path = config["processed_data_path"]
    download_and_preprocess_data(url, unprocessed_data_path, processed_data_path)
