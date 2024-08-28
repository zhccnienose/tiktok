from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app.api.models import r
from app.api.models.comments import CommentModel
from app.api.schema.comment.delete_sha import delete_sha
from app.api.utils.res import res


class CommentDelete(Resource):
    @jwt_required()
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parses = delete_sha(parser)

            if parses['comment_id']:
                r.delete('comments:' + parses['comment_id'])
                comment = CommentModel.get_by_cid(int(parses['comment_id']))
                list_comments = [comment]
                # 删除评论及子评论
                while list_comments:
                    for comment in list_comments:
                        list_comments.extend(CommentModel.get_by_parent_cid(comment.id))
                        comment.delete()
                        list_comments.remove(comment)
            if parses['video_id']:
                CommentModel.delete_by_vid(int(parses['video_id']))
            return res(200, 200, "success")
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
