from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app.api.models.comments import CommentModel
from app.api.schema.comment.list_sha import list_sha
from app.api.utils.res import res


class CommentList(Resource):
    @jwt_required()
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parses = list_sha(parser)

            comments = []
            if parses['video_id']:
                if 'page_num' in parses.keys() and 'page_size' in parses.keys():
                    comments = CommentModel.get_by_vid(int(parses['video_id']), parses['page_size'], parses['page_num'])
                else:
                    comments = CommentModel.get_by_vid(int(parses['video_id']))
            else:
                comments = [CommentModel.get_by_cid(parses['comment_id'])]

            res_data = []
            # print(comments)
            for comment in comments:
                res_data.append(comment.data())

            return res(200, 200, "success", data={"items": res_data})
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
