import logging
import sys
import json


def get_default_logger(instance_name=__name__):
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
