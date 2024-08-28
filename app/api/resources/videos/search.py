from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app.api.models.videos import Videos
from app.api.schema.video.search_sha import search_sha
from app.api.utils.res import res


class VideoSearch(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parses = search_sha(parser)

            videos = Videos.get_by_keyword(**parses)

            return res(status=200,
                       code=200,
                       msg="success",
                       data={"total": len(videos),
                             "items": [video.data() for video in videos]})
        except Exception as e:
            return res(500, 500, str(e))
