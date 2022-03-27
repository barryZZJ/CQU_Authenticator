from time import time


def timestamp():
    return int(time())


def timestamp_ms():
    return int(time() * 1000)
