import logging as log


def get_envs():

    envs = []

    obj = {
        "name": "devenv",
        "descr": "Test cluster",
        "giturl": "https://github.com/migrx-io/projectset-crds.git",
        "env": "test-ocp-cluster",
        "ps_path": "test-ocp/templates",
        "ps_count": "10",
        "pst_path": "test-ocp/crds",
        "pst_count": "20",
    }

    for i in range(20):
        obj["name"] = obj["name"] + f"{i}"
        envs.append(obj)

    log.debug("get_envs..")

    return envs
