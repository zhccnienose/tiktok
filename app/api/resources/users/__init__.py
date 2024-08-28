from flask import Blueprint
from flask_restful import Api

from .avatar import avatar_bp
from .register import UserRegister
from .login import UserLogin
from .refreshtoken import RefreshToken
from .info import UsersInfo

user_bp = Blueprint('users', __name__)
user = Api(user_bp)

user_bp.register_blueprint(avatar_bp, url_prefix='/avatar')

user.add_resource(UserRegister, '/register')
user.add_resource(UserLogin, '/login')
user.add_resource(RefreshToken, "/refreshtoken")

user.add_resource(UsersInfo, '/info')
