from flask import Blueprint
from flask_restful import Api

from .headimages import UserAvatar
from .upload import UserAvatarUpload

avatar_bp = Blueprint('avatar', __name__)
avatar = Api(avatar_bp)

avatar.add_resource(UserAvatar, '/<img_name>')
avatar.add_resource(UserAvatarUpload, '/upload')
