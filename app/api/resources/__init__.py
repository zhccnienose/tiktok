from flask import Blueprint
from .users import user_bp
from .tapi import test_bp
from .videos import video_bp
from .auth import auth_bp
from .comment import comment_bp
from .like import like_bp
from .interact import interact_bp
from .friend import friend_bp

bp = Blueprint('api', __name__)

bp.register_blueprint(test_bp, url_prefix='/test')
bp.register_blueprint(user_bp, url_prefix='/user')
bp.register_blueprint(video_bp, url_prefix='/video')
bp.register_blueprint(auth_bp, url_prefix='/auth')
bp.register_blueprint(comment_bp, url_prefix='/comment')
bp.register_blueprint(like_bp, url_prefix='/like')
bp.register_blueprint(interact_bp, url_prefix='/')
bp.register_blueprint(friend_bp, url_prefix='/friends')