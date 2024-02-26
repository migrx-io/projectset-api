import logging as log
import time
import threading
import os


def loop_unfinished_pull(args):
    threading.Thread(target=_loop_unfinished_pull, args=(args, ),
                     daemon=True).start()


def _loop_unfinished_pull(args):

    _, q = args[0], args[1]

    while True:

        log.debug("start loop_unfinished_pull..")

        q.put("ping")

        time.sleep(int(os.environ.get("PWORKERS_SLEEP", "15")))


def pull(req):

    db, q = req

    # read message from q
    data = q.get()

    log.debug("pull_git_worker: data: %s", data)

    try:

        ok = process_state(db, data)

        log.debug("process_state: result: %s", ok)

    except Exception as e:
        log.error("process_state: ERROR: %s", e)

    return "ok"


def clone_pull_repo():
    pass


def process_state(db, data):

    log.debug("process_state: db: %s, data: %s", db, data)

    return True
