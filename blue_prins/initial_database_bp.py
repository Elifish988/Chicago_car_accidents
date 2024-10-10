from flask import Blueprint

from repository.csv_repository import init_accidents

bp_init = Blueprint('bp_init', __name__)


@bp_init.route('/init/', methods=['GET'])
def init():
    return init_accidents()



