import logging as log
import time
import threading
from datetime import datetime
import os


def _update_task(db, **kwargs):

    if kwargs.get("status") == "":
        kwargs["status"] = "PENDING"

    with db.get_conn() as con:

        if kwargs.get("date_type") == "date_begin":

            con.execute("""
                        UPDATE tasks
                            SET op = '{}', status = '{}', error = '{}', {} = '{}', date_end = ''
                        WHERE uuid = '{}'
                        """.format(kwargs.get("op"), kwargs.get("status"),
                                   kwargs.get("error"),
                                   kwargs.get("date_type"), kwargs.get("date"),
                                   kwargs.get("uuid")))
        else:
            con.execute("""
                        UPDATE tasks
                            SET op = '{}', status = '{}', error = '{}', {} = '{}'
                        WHERE uuid = '{}'
                        """.format(kwargs.get("op"), kwargs.get("status"),
                                   kwargs.get("error"),
                                   kwargs.get("date_type"), kwargs.get("date"),
                                   kwargs.get("uuid")))


def _get_all_tasks(db):

    tasks = []

    log.debug("_get_all_tasks..")
    with db.get_conn() as con:
        cur = con.execute("""
                          SELECT *
                           FROM tasks
                          """)
        for r in cur:
            log.debug(r)
            if r["status"] not in ["FINISHED"]:
                tasks.append(r)

    return tasks


def loop_unfinished_tasks(args):
    threading.Thread(target=_loop_unfinished_tasks, args=(args, ),
                     daemon=True).start()


def _loop_unfinished_tasks(args):

    db, q = args[0], args[1]

    while True:

        log.debug("start loop_unfinished_tasks..")

        tasks = _get_all_tasks(db)
        for t in tasks:
            q.put({"uuid": t["uuid"], "op": t["op"]})

        time.sleep(int(os.environ.get("PWORKERS_SLEEP", "15")))


def push(req):

    db, q = req

    # read message from q

    data = q.get()

    log.debug("pull_git_worker: data: %s", data)

    try:

        ok = process_state(db, data)

        log.debug("process_state: result: %s", ok)

        if ok:
            _update_task(db,
                         uuid=data["uuid"],
                         op=data["op"],
                         status="FINISHED",
                         error="",
                         date_type="date_end",
                         date=datetime.now())

    except Exception as e:
        log.error("process_state: ERROR: %s", e)

        _update_task(db,
                     uuid=data["uuid"],
                     op=data["op"],
                     status="ERROR",
                     error=str(e),
                     date_type="date_end",
                     date=datetime.now())

    return "ok"


def process_state(db, data):

    log.debug("process_state: db: %s, data: %s", db, data)

    return True
