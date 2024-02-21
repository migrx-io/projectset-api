import logging as log
import yaml
import os


def get_envs():

    envs = []

    with open(os.environ.get("APP_CONF", "app.yaml"), 'r',
              encoding="utf-8") as file:

        data = yaml.safe_load(file)

        log.debug("get_envs: data: %s", data)

        envs = data.get('repos', [])

        log.debug("get_envs: %s", envs)

    return envs
