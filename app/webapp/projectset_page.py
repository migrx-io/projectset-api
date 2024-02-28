import logging as log
from flask import Blueprint, render_template, request
from app.util.auth import jwt_required
from app.crds.projectsets import (
    get_projectset,
    create_projectset,
    update_projectset,
    show_projectset,
    delete_projectset,
)
from app.crds.repos import get_envs

projectset_page = Blueprint('projectset_page', __name__)


@projectset_page.route('/', methods=['GET'])
@jwt_required(True)
def projectset():

    projectset_list = get_projectset()

    return render_template('projectset_page.html',
                           projectset_list=projectset_list)


@projectset_page.route('/create', methods=['GET', 'POST'])
@jwt_required(True)
def create():

    if request.method == 'POST':

        repo = request.form.get('repo')
        env = request.form.get('env')
        data = request.form.get('data')

        log.debug("create: data: %s", data)

        try:
            create_projectset(repo, env, data)

        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    # get repos and envs
    envs = get_envs()
    envs = [{"name": k, "url": v["url"]} for k, v in envs.items()]

    return render_template('modal_projectset_upsert_page.html',
                           envs=envs,
                           data="")


@projectset_page.route('/edit/<crd_id>', methods=['GET', 'POST'])
@jwt_required(True)
def edit(crd_id):

    if request.method == 'POST':

        data = request.form.get('data')

        log.debug("create: data: %s", data)

        try:
            update_projectset(crd_id, data)
        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    log.debug("read current state: %s", crd_id)
    data, env = show_projectset(crd_id)
    return render_template('modal_projectset_upsert_page.html',
                           envs=env,
                           data=data)


@projectset_page.route('/delete/<crd_id>', methods=['POST'])
@jwt_required(True)
def delete(crd_id):

    log.debug("delete: crd_id: %s", crd_id)

    try:
        delete_projectset(crd_id)
    except Exception as e:
        return {"error": str(e)}
    # pass
    return {"status": "ok"}
