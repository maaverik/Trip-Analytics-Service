import logging
import sys
import json
import re


def get_default_logger(instance_name: str = __name__):
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)s: \t%(message)s")
    log_handler.setFormatter(formatter)

    logger = logging.getLogger(instance_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    return logger


def get_config():
    file_object = open("config.json", "r")
    config = json.load(file_object)
    return config


def is_valid_iso_date(date: str):
    date_format = r"[\d]{4}-[\d]{2}-[\d]{2}$"
    return bool(re.match(date_format, date))
