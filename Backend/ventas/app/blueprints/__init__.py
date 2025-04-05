from flask import Blueprint
from flask_openapi3 import APIBlueprint

api = APIBlueprint('api', __name__)  # Root API blueprint
plan_blueprint = APIBlueprint('planes', __name__, url_prefix='/planes')
seller_blueprint = APIBlueprint('vendedores', __name__, url_prefix='/planes/<int:plan_id>/vendedores')
command_bp = Blueprint('commands', __name__)

# Import route modules after blueprint creation
from . import sales_plan, sellers, health
