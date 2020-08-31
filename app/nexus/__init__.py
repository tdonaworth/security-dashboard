from flask import Blueprint

bp = Blueprint("nexus", __name__)

from app.nexus import routes, nexusresult
