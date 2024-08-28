from flask import Blueprint
from flask_restful import Api

from .publish import CommentPublish
from .delete import CommentDelete
from .list import CommentList

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')
comment = Api(comment_bp)

comment.add_resource(CommentPublish, '/publish', methods=['POST'])
comment.add_resource(CommentDelete, '/delete', methods=['DELETE'])
comment.add_resource(CommentList, "/list", methods=['GET'])
