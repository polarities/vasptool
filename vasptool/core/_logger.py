import logging, sys

format = "[%(filename)s:%(lineno)s - %(name)s.%(funcName)s] %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format=format)


def get_logger(name):
    return logging.getLogger(name)
