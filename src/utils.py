import logging
import sys


def get_default_logger(instance_name):
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)s: \t%(message)s")
    log_handler.setFormatter(formatter)

    logger = logging.getLogger(instance_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    return logger
