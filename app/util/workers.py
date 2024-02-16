import logging as log
import time
import os


def run_worker(data):

    log.debug("start prcessing: data: %s", data)

    time.sleep(int(os.environ.get("PWORKERS_SLEEP", "15")))
