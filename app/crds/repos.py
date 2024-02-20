import logging as log
import yaml
import os


def get_envs():

    envs = []

    # data = yaml.safe_load(os.environ.get("APP_CONF", "app.yaml"))

    # log.debug("get_envs: data: %s", data)

    # envs = data.get('repos', []) 
    
    log.debug("get_envs: %s", envs)

    return envs
