import logging as log
import yaml
import base64
import app
from app.util.push_worker import create_task, update_task
import json


def get_projectset():

    crds = []

    # get projectset and tasks
    with app.db.get_conn() as con:

        log.debug("exec insert projectset..")

        sql = """SELECT ps.*, t.status, t.op
                 FROM projectset ps, tasks t
                 WHERE ps.uuid = t.uuid"""

        log.debug("sql: %s", sql)

        ps = con.execute(sql)

        for p in ps:

            log.debug("p: %s", p)

            p["labels"] = json.loads(p["labels"])
            p["annotations"] = json.loads(p["annotations"])

            crds.append(p)

    log.debug("get_crds..")

    return crds


def build_tags(labels):

    log.debug("build tags: %s", labels)

    label_tags = []
    for k, v in labels.items():
        label_tags.append(f"{k}={v}")

    return label_tags


# def clear_projectsets(repo, env):
#     # clear data for refresh from git
#     with app.db.get_conn() as con:
#
#         sql = """DELETE FROM projectset as ps
#                  WHERE ps.repo = '{}' AND ps.env = '{}'
#                    AND ps.uuid IN
#                    (SELECT t.uuid FROM tasks as t WHERE t.status == 'FINISHED')""".format(
#             repo, env)
#
#         log.debug("clear_projectsets: %s", sql)
#
#         con.execute(sql)
#
#         sql = """DELETE FROM tasks as t
#                  WHERE t.uuid NOT IN
#                   (SELECT ps.uuid
#                   FROM projectset as ps WHERE ps.repo = '{}' AND ps.env = '{}')""".format(
#             repo, env)
#
#         con.execute(sql)


def create_projectset(repo, env, ydata, silent=False):

    log.debug("create_projectset: repo: %s, env: %s data: %s", repo, env,
              ydata)

    data = yaml.safe_load(ydata)
    log.debug("get_yaml: data: %s", data)

    name = data.get("metadata", {}).get("name")

    uid = base64.b64encode(
        f"{repo},{env},{name}".encode("utf-8")).decode("utf-8")

    log.debug("uid: %s", uid)

    ## if exist - silent return
    _, e = show_projectset(uid)

    if len(e) > 0 and silent:
        return

    if len(e) > 0 and not silent:
        raise Exception("ProjectSet already exists")

    # insert to projectset and tasks
    with app.db.get_conn() as con:

        log.debug("exec insert projectset..")

        sql = """INSERT OR IGNORE INTO
                                  projectset(
                                        uuid,
                                        repo,
                                        env,
                                        name,
                                        template,
                                        labels,
                                        annotations,
                                        data)
                              VALUES('{}',
                                     '{}',
                                     '{}',
                                     '{}',
                                     '{}',
                                     '{}',
                                     '{}',
                                     '{}'
                                     );

                               """.format(
            uid, repo, env, name,
            data.get("spec", {}).get("template"),
            json.dumps(build_tags(data.get("spec", {}).get("labels"))),
            json.dumps(build_tags(data.get("spec", {}).get("annotations"))),
            ydata)

        log.debug("sql: %s", sql)

        con.execute(sql)

        create_task(app.db,
                    uuid=uid,
                    type="projectset",
                    op="CREATE",
                    status="PENDING")
        # app.q_push.put({"uuid": uid, "type": "projectset", "op": "CREATE"})


def update_projectset_status(repo, env, remote_br):

    with app.db.get_conn() as con:

        log.debug("exec insert projectset..")

        sql = """SELECT * FROM projectset as ps
                  WHERE ps.repo  = '{}' AND ps.env = '{}'; """.format(
            repo, env)

        ps = con.execute(sql)

        uuids = []
        all_uuids = []
        for p in ps:

            log.debug("p: %s", p)
            if p["name"] in remote_br:
                uuids.append(p["uuid"])
            else:
                all_uuids.append(p["uuid"])

        for uid in uuids:

            sql = """UPDATE tasks SET status = 'WAITING_APPROVAL'
                    WHERE uuid  = '{}';""".format(uid)

            con.execute(sql)

        # update other to finished
        for uid in all_uuids:

            sql = """UPDATE tasks SET status = 'FINISHED'
                    WHERE uuid  = '{}';""".format(uid)
            con.execute(sql)


def update_projectset(crd_id, ydata):
    log.debug("update_projectset: crd_id: %s,data %s", crd_id, ydata)

    data = yaml.safe_load(ydata)

    ## if exist - silent return
    _, e = show_projectset(crd_id)

    if len(e) > 0 and e[0]["status"] != "FINISHED":
        raise Exception("There is one PR already exists")

    log.debug("update data: %s", data)

    with app.db.get_conn() as con:

        log.debug("exec insert projectset..")

        sql = """UPDATE projectset SET data = '{}',
                                       labels = '{}',
                                       annotations = '{}',
                                       template = '{}'
                 WHERE uuid = '{}'
                               """.format(
            ydata, json.dumps(build_tags(data.get("spec", {}).get("labels"))),
            json.dumps(build_tags(data.get("spec", {}).get("annotations"))),
            data.get("spec", {}).get("template"), crd_id)

        log.debug("update sql: %s", sql)

        con.execute(sql)

    update_task(app.db,
                uuid=crd_id,
                op="UPDATE",
                status="PENDING",
                date_type="date_begin")

    app.q_push.put({"uuid": crd_id, "type": "projectset", "op": "UPDATE"})


def show_projectset(crd_id):
    log.debug("show_projectset: crd_id %s", crd_id)

    dyaml = ""
    env = []

    with app.db.get_conn() as con:

        log.debug("select projectset..")

        sql = """SELECT ps.*, t.status
                 FROM projectset ps, tasks t
                 WHERE ps.uuid = t.uuid and ps.uuid = '{}'""".format(crd_id)

        cur = con.execute(sql)

        for i in cur.fetchall():
            log.debug("fetchall: %s", i)
            dyaml = i["data"]
            env.append({
                "url": i["repo"],
                "name": i["env"],
                "status": i["status"]
            })

    return dyaml, env


def delete_projectset(crd_id):
    log.debug("delete_projectset: crd_id %s", crd_id)

    ## if exist - silent return
    _, e = show_projectset(crd_id)

    if len(e) > 0 and e[0]["status"] != "FINISHED":
        raise Exception("There is one PR already exists")

    update_task(app.db,
                uuid=crd_id,
                op="DELETE",
                status="PENDING",
                date_type="date_begin")

    app.q_push.put({"uuid": crd_id, "type": "projectset", "op": "DELETE"})
