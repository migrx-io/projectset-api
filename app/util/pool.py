import threading
import logging as log
import time


class Pool:

    def __init__(self, size, func, data):
        self.size = size
        self.func = func
        self.data = data

    def start(self):
        for _ in range(self.size):
            threading.Thread(target=process,
                             args=(self.func, self.data),
                             daemon=True).start()


def process(f, data):

    while True:

        try:
            res = f(data)
            log.debug(res)

        except Exception as e:
            log.error(e)
            time.sleep(5)
