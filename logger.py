import logging
import sys


def get_logger(name=__file__, file='app.log', encoding='utf-8'):
    log = logging.getLogger(name)

    fh = logging.FileHandler(file, encoding=encoding)
    log.addHandler(fh)

    sh = logging.StreamHandler(stream=sys.stdout)
    log.addHandler(sh)
    return log
