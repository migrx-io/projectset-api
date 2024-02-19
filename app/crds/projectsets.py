import logging as log


def get_projectset():

    crds = [
            {
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
            },

            {
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
            }
 
            ]


    # transform labels to tags
    for crd in crds:

        labels = crd.get("labels", {})
        annotations = crd.get("annotations", {})

        label_tags = []
        for k, v in labels.items():
            label_tags.append("{}={}".format(k, v))

        annotation_tags = []
        for k, v in annotations.items():
            annotation_tags.append("{}={}".format(k, v))


        crd["label_tags"] = label_tags
        crd["annotation_tags"] = annotation_tags

    log.debug("get_crds..")

    return crds


def create():
    pass


def delete():
    pass
