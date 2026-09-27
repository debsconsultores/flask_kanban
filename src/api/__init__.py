# from flask import Blueprint
from flask_smorest  import Blueprint

bp = Blueprint(
    'api',
    __name__,
    url_prefix="/api/v1"
    )


from src.api import routes