import logging
from src.utils import get_config, get_default_logger, is_valid_iso_date


def test_config():
    config = get_config()
    assert "dataset_download_url" in config
    assert "unprocessed_data_path" in config
    assert "processed_data_path" in config


def test_get_default_logger():
    logger = get_default_logger()
    assert isinstance(logger, logging.Logger)


def test_is_valid_iso_date():
    assert is_valid_iso_date("2020-01-01") is True
    assert is_valid_iso_date("2020-01-1") is False
    assert is_valid_iso_date("01-01-2020") is False
