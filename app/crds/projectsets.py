import logging as log


def get_projectset():

    crds = [{
        "repo": "https://github.com/migrx-io/projectset-crds.git",
        "env": "test-ocp-cluster",
        "name": "dev-app",
        "template": "dev-small",
        "labels": {
            "app.kubernetes.io/name": "projectset2",
            "app.kubernetes.io/instance": "projectse2t",
            "app.kubernetes.io/part-of": "projectset-operator",
            "app.kubernetes.io/managed-by": "kustomize",
            "app.kubernetes.io/created-by": "projectset-operator"
        },
        "annotations": {
            "app.kubernetes.io/name": "projectset2",
            "app.kubernetes.io/instance": "projectset2",
            "app.kubernetes.io/part-of": "projectset-operator",
            "app.kubernetes.io/managed-by": "kustomize",
            "app.kubernetes.io/created-by": "projectset-operator"
        },
    }, {
        "repo": "https://github.com/migrx-io/projectset-crds.git",
        "env": "prod-ocp-cluster",
        "name": "prod-app",
        "template": "dev-mid",
        "labels": {
            "app.kubernetes.io/name": "projectset",
            "app.kubernetes.io/instance": "projectset",
            "app.kubernetes.io/part-of": "projectset-operator",
            "app.kubernetes.io/managed-by": "kustomize",
            "app.kubernetes.io/created-by": "projectset-operator"
        },
        "annotations": {
            "app.kubernetes.io/name": "projectset",
            "app.kubernetes.io/instance": "projectset",
            "app.kubernetes.io/part-of": "projectset-operator",
            "app.kubernetes.io/managed-by": "kustomize",
            "app.kubernetes.io/created-by": "projectset-operator"
        },
    }]

    # transform labels to tags
    for crd in crds:

        labels = crd.get("labels", {})
        annotations = crd.get("annotations", {})

        label_tags = []
        for k, v in labels.items():
            label_tags.append(f"{k}={v}")

        annotation_tags = []
        for k, v in annotations.items():
            annotation_tags.append(f"{k}={v}")

        crd["label_tags"] = label_tags
        crd["annotation_tags"] = annotation_tags

    log.debug("get_crds..")

    return crds

def build_tags(labels):

    label_tags = []
    for k, v in labels.items():
        label_tags.append(f"{k}={v}")

    return label_tags

 


def create_projectset(repo, env, yaml):

    log.debug("create_projectset: repo: %s, env: %s data: %s",repo, env, yaml)

    data = yaml.safe_load(yaml)
    log.debug("get_yaml: data: %s", data)

    # insert to projectset and tasks
    """
    with app.db.get_conn() as con:

        con.execute(INSERT INTO
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
                               ).format(task_uuid, name, "CREATE", "", "",
                                           sct_config, dms_config, sql, "", "",
                                           ""))

    _update_task(app.db, task_uuid, "CREATE", "", "", "date_begin",
                 datetime.now())

    app.q_dms.put({"uuid": task_uuid, "name": name, "op": "CREATE"})
    return task_uuid
    """

def update_projectset(crd_id, data):
    log.debug("update_projectset: crd_id: %s,data %s", crd_id, data)


def show_projectset(crd_id):
    log.debug("show_projectset: crd_id %s", crd_id)

    yaml = """
    name: test

    """

    return yaml


def delete_projectset(crd_id):
    log.debug("delete_projectset: crd_id %s", crd_id)
