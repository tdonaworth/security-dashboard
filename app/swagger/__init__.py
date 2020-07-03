from flask import Blueprint

bp = Blueprint('swagger', __name__)

from app.swagger import swagger