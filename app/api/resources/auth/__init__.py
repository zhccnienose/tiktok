from flask import Blueprint
from flask_restful import Api

from .mfa import mfa_bp

auth_bp = Blueprint('auth', __name__)
auth = Api(auth_bp)

auth_bp.register_blueprint(mfa_bp, url_prefix='/mfa')
