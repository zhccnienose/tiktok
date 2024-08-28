from flask import Flask
from flask_jwt_extended import JWTManager

from .config import Config
from .api.models import db, r
from .api.resources import bp

from .manage import migrate
from .api.models.users import UserModel
from .api.models.comments import CommentModel
from .api.models.videos import Videos


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)
    if testing:
        app.config['TESTING'] = True
    app.register_blueprint(bp)

    db.init_app(app)
    migrate.init_app(app, db)

    jwt = JWTManager(app)
    register_jwt_hooks(jwt)
    return app


def register_jwt_hooks(jwt):
    # 过期返回信息
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, decrypted_token):
        return {
            'code': 403,
            'message': 'expired token'
        }

    # 验证失败返回信息
    @jwt.invalid_token_loader
    def invalid_token_callback(jwt_header, decrypted_token):
        return {
            'code': 400,
            'message': 'Invalid token'
        }

    # 缺少token返回信息
    @jwt.unauthorized_loader
    def missing_token_callback(decrypted_token):
        return {
            "code": 401,
            "msg": "Missing token"
        }


app = create_app()
