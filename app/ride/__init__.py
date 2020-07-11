from flask import Blueprint

bp = Blueprint('ride', __name__)

from app.ride import routes
