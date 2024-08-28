from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app.api.models import r
from app.api.models.videos import Videos
from app.api.schema.video.hot_sha import hot_sha
from app.api.utils.res import res


class VideoHot(Resource):
    @jwt_required()
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parses = hot_sha(parser)

            videos_id = [int(vid.decode("utf-8").split("_")[0]) for vid in r.zrange("list_hot", 0, -1, desc=True)]
            total = len(videos_id)
            # 若页码超出范围，则返回最后一页
            if parses['page_num'] * parses['page_size'] > total:
                parses['page_num'] = total // parses['page_size'] -1
                if total % parses['page_size']:
                    parses['page_num'] -= 1

            videos = []
            try:
                videos = Videos.get_by_vids(videos_id, parses['page_num'], parses['page_size'])
            except Exception as e:
                print(str(e))

            return res(status=200, code=200, msg="success", data={"items": [videos.data() for videos in videos]})
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
