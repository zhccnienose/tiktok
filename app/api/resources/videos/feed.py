from flask_restful import Resource, reqparse

from app.api.models.videos import Videos
from app.api.utils.res import res


# 视频流
class VideoFeed(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('latest_time', type=str, required=False, location="args")
            parses = parser.parse_args()

            if not parses['latest_time']:
                videos = Videos.all()
            else:
                videos = Videos.get_by_time(parses['latest_time'])
            res_data = []
            if not videos:
                for video in videos:
                    res_data.append(video.data())

            return res(200, 200, "success", {"items": res_data})
        except Exception as e:
            return res(500, 500, str(e))
