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

        sql = """SELECT ps.*, t.status
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


def create_projectset(repo, env, ydata):

    log.debug("create_projectset: repo: %s, env: %s data: %s", repo, env,
              ydata)

    data = yaml.safe_load(ydata)
    log.debug("get_yaml: data: %s", data)

    name = data.get("metadata", {}).get("name")

    uid = base64.b64encode(
        f"{repo},{env},{name}".encode("utf-8")).decode("utf-8")

    log.debug("uid: %s", uid)

    # insert to projectset and tasks
    with app.db.get_conn() as con:

        log.debug("exec insert projectset..")

        sql = """INSERT INTO
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

        create_task(app.db, uuid=uid, op="CREATE", status="PENDING")

        app.q_git.put({"uuid": uid, "op": "CREATE"})


def update_projectset(crd_id, ydata):
    log.debug("update_projectset: crd_id: %s,data %s", crd_id, ydata)

    data = yaml.safe_load(ydata)

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

    app.q_git.put({"uuid": crd_id, "op": "UPDATE"})


def show_projectset(crd_id):
    log.debug("show_projectset: crd_id %s", crd_id)

    dyaml = ""
    env = []

    with app.db.get_conn() as con:

        log.debug("select projectset..")

        sql = """SELECT * FROM projectset
                 WHERE uuid = '{}'""".format(crd_id)

        cur = con.execute(sql)

        for i in cur.fetchall():
            log.debug("fetchall: %s", i)
            dyaml = i["data"]
            env.append({"url": i["repo"], "name": i["env"]})

    return dyaml, env


def delete_projectset(crd_id):
    log.debug("delete_projectset: crd_id %s", crd_id)

    update_task(app.db,
                uuid=crd_id,
                op="DELETE",
                status="PENDING",
                date_type="date_begin")

    app.q_git.put({"uuid": crd_id, "op": "DELETE"})
