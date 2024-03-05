import logging as log
import os
import traceback
from pathlib import Path
import yaml
from app.crds.repos import get_envs
from app.util.exec import run_shell
from app.crds.projectsets import create_projectset, update_projectset_status

# def loop_unfinished_pull(args):
#     threading.Thread(target=_loop_unfinished_pull, args=(args, ),
#                      daemon=True).start()

# def _loop_unfinished_pull(args):
#
#     _, q = args[0], args[1]
#     while True:
#         log.debug("start loop_unfinished_pull..")
#         q.put("ping")
#         time.sleep(int(os.environ.get("PWORKERS_SLEEP", "15")))


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


def _parse_clone_dir(repo_url, repo_dir, myaml, remote_br):

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

                if t.find("gitignore") >= 0:
                    continue

                # for t in glob.glob("."):
                log.debug("read projectset: %s", t)

                with open("{}/{}".format(template_dir, t),
                          "r",
                          encoding="utf-8") as f:
                    data = f.read()

                    log.debug("DATA: %s", data)

                    create_projectset("projectset_template", repo_url, name,
                                      data, True)

        # update if remote_dr exists
        update_projectset_status("projectset_template", repo_url, name,
                                 remote_br)

        #
        # project set
        #

        dirt = Path(projectset_dir)
        # clear before iterate
        # clear_projectsets(repo_url, name)

        if dirt.exists():
            log.debug("exists")

            for t in os.listdir(projectset_dir):

                if t.find("gitignore") >= 0:
                    continue

                # for t in glob.glob("."):
                log.debug("read projectset: %s", t)

                with open("{}/{}".format(projectset_dir, t),
                          "r",
                          encoding="utf-8") as f:
                    data = f.read()

                    log.debug("DATA: %s", data)

                    create_projectset("projectset", repo_url, name, data, True)

        # update if remote_dr exists
        update_projectset_status("projectset", repo_url, name, remote_br)


def clone_pull_repo():

    env_list = get_envs()
    log.debug("env_list: %s", env_list)

    for k, v in env_list.items():
        log.debug("chekc and pull %s", v)

        dir_name = "/tmp/" + k
        url_auth = "https://{}:{}@{}".format("projectset-api", v["token"],
                                             v["url"][8:])

        repo_dir = "{}/{}".format(dir_name, v["url"].split("/")[-1][:-4])

        log.debug("dir_name: %s, url_auth: %s", dir_name, url_auth)

        directory = Path(repo_dir)
        if directory.exists():
            log.debug("exists")

            ok, err = run_shell("cd {} && git remote set-url origin {}".format(
                repo_dir, url_auth))

        else:
            log.debug("clone..")
            directory.mkdir(parents=True, exist_ok=True)

            # clone to dir
            ok, err = run_shell("cd {} && git clone {}".format(
                dir_name, url_auth))
            log.debug("ok: %s, err: %s", ok, err)

        # checkout to main before pull
        ok, err = run_shell(
            "cd {} && git checkout {} && git checkout -- * && git pull".format(
                repo_dir, v["branch"]))
        log.debug("ok: %s, err: %s", ok, err)

        # update remote and local branches
        remote_br = update_branches(repo_dir, v)

        # read repo manifest
        manifest_file = "{}/{}".format(repo_dir, v["conf_file"])

        log.debug("read manifests file: %s", manifest_file)

        dirt = Path(manifest_file)
        if dirt.exists():
            log.debug("exists")

            myaml = {}
            with open(manifest_file, "r", encoding="utf-8") as f:
                myaml = yaml.safe_load(f)

            log.debug("manifest: %s", myaml)

            # iterate thru env
            _parse_clone_dir(v["url"], repo_dir, myaml, remote_br)


def update_branches(repo_dir, v):

    # prune remote first
    ok, err = run_shell("cd {} && git fetch origin --prune".format(repo_dir))
    log.debug("prune: ok: %s err: %s", ok, err)

    _, data = run_shell("cd {} && git branch -a".format(repo_dir))

    local_br = {}
    remote_br = {}

    for i in data.decode("utf-8").split("\n"):
        log.debug("update_branches: %s", i)

        branch = i.split("/")
        if i.find("remotes/origin") != -1:
            remote_br[branch[2]] = True
        else:
            local_br[branch[0]] = True

    log.debug("update_branches: local_br: %s , remote_br: %s", local_br,
              remote_br)
    log.debug("update_branches: main is: %s", v["branch"])

    for k in local_br:

        if remote_br.get(k) is None and k.find(v["branch"]) == -1 and k != "":
            # delete branch if not exists

            log.debug("delete branch %s", k)
            ok, err = run_shell("cd {} && git branch -D {}".format(
                repo_dir, k))

    return remote_br.keys()


def process_state(db, data):

    log.debug("process_state: db: %s, data: %s", db, data)
    clone_pull_repo()

    return True
