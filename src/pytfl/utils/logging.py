# ^=_ coding: utf-8 _=^

import logging
import sys

logging_format = "%(asctime)-15s | %(levelname)-5s | %(name)-19s | %(message)s"
logging.basicConfig(level=logging.INFO, format=logging_format, stream=sys.stderr)


def getLogger(name):
    return logging.getLogger(name)
