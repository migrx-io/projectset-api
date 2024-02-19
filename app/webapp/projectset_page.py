from flask import Blueprint, render_template, request
# import app
from app.util.auth import jwt_required
from app.crds.projectsets import get_projectset, create

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

        name = request.form.get('name', "x")

        try:
            create(name)

        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('projectset_create_modal.html')



@projectset_page.route('/edit', methods=['GET', 'POST'])
@jwt_required(True)
def edit():
    pass


@projectset_page.route('/delete', methods=['GET', 'POST'])
@jwt_required(True)
def delete():
    pass
