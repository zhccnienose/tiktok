from datetime import datetime

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.comments import CommentModel
from app.api.models.users import UserModel
from app.api.schema.comment.publish_sha import publish_sha
from app.api.utils.res import res


class CommentPublish(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parses = publish_sha(parser)

            data = {'id': CommentModel.max_id() + 1,
                    'deleted_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'created_at': datetime.now(),
                    'user_id': UserModel.find_by_username(get_jwt_identity()).uid,
                    'content': parses['content']}

            if parses['video_id']:
                r.hincrby(parses['video_id'] + "_" + data['user_id'], "comments", 1)
                data['video_id'] = parses['video_id']
                # 若父评论id参数不存在则置0
                data['parent_id'] = parses['comment_id'] if parses['comment_id'] else 0
            else:
                data['parent_id'] = parses['comment_id']
                data['video_id'] = CommentModel.get_by_cid(parses['comment_id']).video_id
                print('------1------')
                r.hincrby(str(data['video_id']) + "_" + data['user_id'], "comments", 1)
                print('------2------')
            if parses['comment_id'] and parses['comment_id'] != "0":
                comment = CommentModel.get_by_cid(parses['comment_id'])
                # 回溯父评论，子评论数+1
                r.hincrby("comments:" + str(comment.id), "child_count", 1)
                while comment:
                    r.hincrby("comments:" + str(comment.id), "child_count", 1)
                    comment = CommentModel.get_by_cid(comment.parent_id)

            r.hmset('comments:' + str(data['id']), {"like_count": 0, "child_count": 0})

            comment = CommentModel(**data)
            comment.add_comment()

            return res(200, 200, "success")
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
