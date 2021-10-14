import logging
from src.utils import get_config, get_default_logger


def test_config():
    config = get_config()
    assert "dataset_download_url" in config
    assert "unprocessed_data_path" in config
    assert "processed_data_path" in config


def test_get_default_logger():
    logger = get_default_logger()
    assert isinstance(logger, logging.Logger)
