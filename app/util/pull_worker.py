import logging as log
import time
import threading
import os
import traceback
from pathlib import Path
import yaml
from app.crds.repos import get_envs
from app.util.exec import run_shell
from app.crds.projectsets import create_projectset


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
        log.error("process_state: ERROR: %s \n %s", e, traceback.format_exc())

    return "ok"


def _parse_clone_dir(repo_url, repo_dir, myaml):

    log.debug("start working on envs..")

    for name, env in myaml.get("envs", []).items():
        log.debug("parse name: %s env: %s", name, env)

        # read templates
        template_dir = "{}/{}".format(repo_dir,
                                      env.get("projectset-templates"))
        projectset_dir = "{}/{}".format(repo_dir, env.get("projectset-crds"))

        log.debug("template_dir: %s, projectset_dir: %s", template_dir,
                  projectset_dir)

        # template
        dirt = Path(template_dir)
        if dirt.exists():
            log.debug("exists")

            for t in os.listdir(template_dir):
                # for t in glob.glob("."):
                log.debug("read template: %s", t)

        # project set
        dirt = Path(projectset_dir)
        if dirt.exists():
            log.debug("exists")

            for t in os.listdir(projectset_dir):
                # for t in glob.glob("."):
                log.debug("read projectset: %s", t)

                with open("{}/{}".format(projectset_dir, t),
                          "r",
                          encoding="utf-8") as f:
                    data = f.read()

                    log.debug("DATA: %s", data)
                    create_projectset(repo_url, name, data, True)


def clone_pull_repo():

    env_list = get_envs()
    log.debug("env_list: %s", env_list)

    for k, v in env_list.items():
        log.debug("chekc and pull %s", v)

        dir_name = "/tmp/" + k
        url_auth = "https://{}:{}@{}".format("projectset-api", v["token"],
                                             v["url"][7:])

        repo_dir = "{}/{}".format(dir_name, v["url"].split("/")[-1][:-4])

        log.debug("dir_name: %s, url_auth: %s", dir_name, url_auth)

        directory = Path(repo_dir)
        if directory.exists():
            log.debug("exists")

        else:
            log.debug("clone..")
            directory.mkdir(parents=True, exist_ok=True)

            # clone to dir
            ok, err = run_shell("cd {} && git clone {}".format(
                dir_name, v["url"]))
            log.debug("ok: %s, err: %s", ok, err)

        ok, err = run_shell("cd {} && git checkout {}".format(
            repo_dir, v["branch"]))
        log.debug("ok: %s, err: %s", ok, err)

        ok, err = run_shell("cd {} && git pull".format(repo_dir))
        log.debug("ok: %s, err: %s", ok, err)

        # read repo manifest
        manifest_file = "{}/{}".format(repo_dir, v["conf_file"])

        log.debug("read manifests file: %s", manifest_file)

        myaml = {}
        with open(manifest_file, "r", encoding="utf-8") as f:
            myaml = yaml.safe_load(f)

        log.debug("manifest: %s", myaml)

        # iterate thru env
        _parse_clone_dir(v["url"], repo_dir, myaml)


def process_state(db, data):

    log.debug("process_state: db: %s, data: %s", db, data)

    clone_pull_repo()

    return True
