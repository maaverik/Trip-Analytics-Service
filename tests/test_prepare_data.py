from unittest.mock import patch
import pandas as pd
import datetime as dt
from src.prepare_data import download_and_preprocess_data


# integration test for data preprocessing
@patch("os.makedirs")
@patch("os.path")
@patch("gdown.download")
@patch("pandas.DataFrame.to_csv")
@patch("pandas.read_parquet")
def test_load_and_process_unprocessed_parquet(
    mock_parquet, mock_csv, mock_download, mock_path, mock_makedirs
):
    dummy_df = pd.DataFrame(
        {
            "unique_key": ["12345"],
            "trip_start_timestamp": [dt.datetime(2020, 1, 5, 0, 1, 2)],
            "trip_end_timestamp": [dt.datetime(2020, 1, 5, 1, 2, 3)],
            "trip_miles": [5],
            "trip_seconds": [300],
            "pickup_latitude": [98.75],
            "pickup_longitude": [99.20],
            "fare": [500],
        }
    )
    mock_parquet.return_value = dummy_df
    download_and_preprocess_data("dummy/url", "./dummy/in/path", "./dummy/out/path")

    mock_parquet.assert_called()
    mock_csv.assert_called()
    mock_download.assert_called()
