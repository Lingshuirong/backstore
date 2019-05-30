from flask import Blueprint


api = Blueprint('api_1_0', __name__, url_prefix='/backstore/api/1.0')

from . import user