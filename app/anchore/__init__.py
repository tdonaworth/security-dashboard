from flask import Blueprint

bp = Blueprint("anchore", __name__)

from app.anchore import routes
