import logging as log


def get_projectset():

    crds = []

    obj = {
        "name": "devenv",
        "labels": "label=value",
        "annotations": "annotations=value",
    }

    for i in range(20):
        obj["name"] = obj["name"] + f"{i}"
        crds.append(obj)

    log.debug("get_crds..")

    return crds


def create():
    pass


def delete():
    pass
