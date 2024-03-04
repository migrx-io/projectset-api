import logging as log
import time
import threading
from datetime import datetime
import os
import base64
import traceback
from pathlib import Path
import yaml
from app.util.exec import run_shell
from app.crds.repos import get_envs


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
            log.debug("_get_all_tasks: %s", r)
            if r["status"] == "PENDING":
                tasks.append(r)

    return tasks


def loop_unfinished_tasks(args):
    threading.Thread(target=_loop_unfinished_tasks, args=(args, ),
                     daemon=True).start()


def _loop_unfinished_tasks(args):

    db, q, q_pull = args[0], args[1], args[2]

    while True:

        log.debug("start loop_unfinished_tasks..")

        try:
            tasks = _get_all_tasks(db)
            for t in tasks:

                log.debug("_loop_unfinished_tasks: %s", t)
                q.put({"uuid": t["uuid"], "type": t["type"], "op": t["op"]})

            # wait between push and pull
            time.sleep(5)

            # trigger pull
            q_pull.put("ping")

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


def clear_tables(db, uid):

    with db.get_conn() as con:
        sql = """DELETE FROM projectset WHERE uuid = '{}';""".format(uid)
        con.execute(sql)

        sql = """DELETE FROM tasks WHERE uuid = '{}';""".format(uid)
        con.execute(sql)


def is_cr_exists(parts):

    env_list = get_envs()
    log.debug("env_list: %s", env_list)

    k = parts[1]
    v = env_list.get(k)

    log.debug("e: %s", v)
    repo_dir = v["url"].split("/")[-1][:-4]
    repo_conf = v["conf_file"]

    dir_name = "/tmp/{}/{}".format(k, repo_dir)
    conf_file = "{}/{}".format(dir_name, repo_conf)

    log.debug("is_cr_exists: dir_name: %s", dir_name)
    log.debug("is_cr_exists: conf_file: %s", conf_file)

    # open conf and check locations
    with open(conf_file, "r", encoding="utf-8") as f:
        ydata = yaml.safe_load(f.read())

    log.debug("is_cr_exists: ydata: %s", ydata)

    cr_dir = ydata.get("envs", {}).get(k, {}).get("projectset-crds")
    log.debug("is_cr_exists: cr_dir: %s", cr_dir)

    cr_dir_path = "{}/{}".format(dir_name, cr_dir)
    dirt = Path("{}/{}.yaml".format(cr_dir_path, parts[2]))
    log.debug("is_cr_exists: dirt: %s", dirt)

    if dirt.exists():
        return True, cr_dir_path, dirt, parts[2], v

    return False, cr_dir_path, dirt, parts[2], v


def process_state(db, data):

    log.debug("process_state: db: %s, data: %s", db, data)

    if data["op"] in ["CREATE", "UPDATE"]:

        # check if exists and eq
        if data["type"] == "projectset":

            ps = show_projectset(db, data["uuid"])

            log.debug("CREATE: data: %s", ps)

            parts = base64.b64decode(data["uuid"]).decode("utf-8").split(",")

            log.debug("parts: %s", parts)

            ok, cr_dir, cr, branch, v = is_cr_exists(parts)

            log.debug("not found file: %s..creating..", cr)

            # set url
            url_auth = "https://{}:{}@{}".format("projectset-api", v["token"],
                                                 v["url"][8:])

            # add new branch
            ok, err = run_shell("cd {} && git remote set-url origin {}".format(
                cr_dir, url_auth))

            log.debug("ok: %s, err: %s", ok, err)

            # add new branch
            ok, err = run_shell("cd {} && git checkout -b {}".format(
                cr_dir, branch))

            log.debug("ok: %s, err: %s", ok, err)

            # create file
            with open(f'{cr}', 'w+', encoding="utf-8") as f:
                f.write(ps["data"])

            ok, err = run_shell(
                f"cd {cr_dir} && git add {cr} && git commit -m 'Create {branch}'"
            )
            log.debug("ok: %s, err: %s", ok, err)

            # push to origin
            ok, err = run_shell("cd {} && git push origin {}".format(
                cr_dir, branch))
            log.debug("ok: %s, err: %s", ok, err)

            ok, err = run_shell("cd {} && git checkout {}".format(
                cr_dir, v["branch"]))
            log.debug("ok: %s, err: %s", ok, err)

            # create MR/PR

            url_parts = v["url"].split("/")

            create_pull_request(v["token"], url_parts[3], url_parts[-1][:-4],
                                f"Create {branch}", f"Delete {branch}",
                                f"{branch}", v["branch"])

    elif data["op"] == "DELETE":

        if data["type"] == "projectset":

            ps = show_projectset(db, data["uuid"])

            log.debug("DELETE: data: %s", ps)

            parts = base64.b64decode(data["uuid"]).decode("utf-8").split(",")

            log.debug("parts: %s", parts)

            ok, cr_dir, cr, branch, v = is_cr_exists(parts)

            if ok:
                log.debug("found file: %s..deleting..", cr)

                # set url
                url_auth = "https://{}:{}@{}".format("projectset-api",
                                                     v["token"], v["url"][8:])

                # add new branch
                ok, err = run_shell(
                    "cd {} && git remote set-url origin {}".format(
                        cr_dir, url_auth))

                log.debug("ok: %s, err: %s", ok, err)

                # add new branch
                ok, err = run_shell("cd {} && git checkout -b {}".format(
                    cr_dir, branch))

                log.debug("ok: %s, err: %s", ok, err)

                # delete file
                ok, err = run_shell(
                    f"cd {cr_dir} && rm -rf {cr} && git rm {cr} && git commit -m 'Delete {branch}'"
                )
                log.debug("ok: %s, err: %s", ok, err)

                # push to origin
                ok, err = run_shell("cd {} && git push origin {}".format(
                    cr_dir, branch))
                log.debug("ok: %s, err: %s", ok, err)

                ok, err = run_shell("cd {} && git checkout {}".format(
                    cr_dir, v["branch"]))
                log.debug("ok: %s, err: %s", ok, err)

                # create MR/PR

                url_parts = v["url"].split("/")

                create_pull_request(v["token"], url_parts[3],
                                    url_parts[-1][:-4], f"Delete {branch}",
                                    f"Delete {branch}", f"{branch}",
                                    v["branch"])

            else:
                log.debug("file not found. clear table")
                clear_tables(db, data["uuid"])

    return True


#
# Github PR
#
def create_pull_request(*args):

    token, owner, repo, title, body, dest, source = args

    cmd = """
    curl -L \
    -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer {}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/{}/{}/pulls \
    -d '{{"title":"{}","body":"{}","head":"{}","base":"{}"}}'
    """.format(token, owner, repo, title, body, dest, source)

    log.debug("create_pull_request: cmd: %s", cmd)

    ok, err = run_shell(cmd)

    log.debug("ok: %s, err: %s", ok, err)
