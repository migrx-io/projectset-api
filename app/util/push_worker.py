import logging as log
import time
import threading
from datetime import datetime
import os
import base64
import traceback


def show_projectset(db, crd_id):
    log.debug("show_projectset: crd_id %s", crd_id)

    env = None

    with db.get_conn() as con:

        log.debug("select projectset..")

        sql = """SELECT * FROM projectset
                 WHERE uuid = '{}'""".format(crd_id)

        cur = con.execute(sql)

        for i in cur.fetchall():
            log.debug("fetchall: %s", i)
            env = {"url": i["repo"], "name": i["env"], "data": i["data"]}

    return env


def create_task(db, **kwargs):
    with db.get_conn() as con:
        con.execute("""
                    INSERT OR IGNORE INTO tasks(uuid, op, type, status)
                    VALUES ('{}', '{}', '{}', '{}')
                    """.format(kwargs.get("uuid"), kwargs.get("op"),
                               kwargs.get('type'), kwargs.get("status")))


def update_task(db, **kwargs):

    if kwargs.get("status") == "":
        kwargs["status"] = "PENDING"

    with db.get_conn() as con:

        if kwargs.get("date_type") == "date_begin":

            log.debug("date_begin..%s", kwargs)

            con.execute("""
                        UPDATE tasks
                            SET op = '{}', status = '{}', error = '{}', {} = '{}', date_end = ''
                        WHERE uuid = '{}'
                        """.format(kwargs.get("op"), kwargs.get("status"),
                                   kwargs.get("error"),
                                   kwargs.get("date_type"), kwargs.get("date"),
                                   kwargs.get("uuid")))
        else:

            log.debug("update: %s", kwargs)

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

        try:
            tasks = _get_all_tasks(db)
            for t in tasks:
                q.put({"uuid": t["uuid"], "type": t["type"], "op": t["op"]})
        except Exception as e:
            log.error("_loop_unfinished_tasks: %s", e)

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
            update_task(db,
                        uuid=data["uuid"],
                        op=data["op"],
                        status="FINISHED",
                        error="",
                        date_type="date_end",
                        date=datetime.now())

    except Exception as e:
        log.error("process_state: ERROR: %s \n %s", e, traceback.format_exc())

        update_task(db,
                    uuid=data["uuid"],
                    op=data["op"],
                    status="ERROR",
                    error=str(e),
                    date_type="date_end",
                    date=datetime.now())

    return "ok"


def process_state(db, data):

    log.debug("process_state: db: %s, data: %s", db, data)

    if data["op"] == "CREATE":

        # check if exists and eq

        if data["type"] == "projectset":
            data = show_projectset(db, data["uuid"])

            log.debug("CREATE: data: %s", data)

        # add new branch

        # create file

        # push to origin

        # create MR/PR

    elif data["op"] == "UPDATE":

        # add new branch

        # create file

        # push to origin

        # create MR/PR
        pass

    elif data["op"] == "DELETE":

        if data["type"] == "projectset":

            ps = show_projectset(db, data["uuid"])

            log.debug("DELETE: data: %s", ps)

            parts = base64.b64decode(data["uuid"]).decode("utf-8").split(",")

            log.debug("parts: %s", parts)

        # add new branch

        # delete file

        # push to origin

        # create MR/PR

    return True
