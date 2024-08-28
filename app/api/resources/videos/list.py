from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app.api.models.videos import Videos
from app.api.schema.video.list_sha import list_sha
from app.api.utils.res import res


# 用户的发布列表
class VideoList(Resource):
    @jwt_required()
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parses = list_sha(parser)

            videos = Videos.get_by_uid(int(parses['user_id']))

            if videos:
                total = len(videos)
                res_data = []
                if total < parses['page_size'] * parses['page_num']:
                    if total <= parses['page_size']:
                        pass
                    else:
                        if total % parses['page_size']:
                            videos = videos[(total // parses['page_size']) * parses['page_size']:]
                        else:
                            videos = videos[total-parses['page_size']:]
                else:
                    if total <= (parses['page_num']+1)*parses['page_size']:
                        videos = videos[parses['page_num'] * parses['page_size']:]
                    else:
                        videos = videos[parses['page_num'] * parses['page_size']:(parses['page_num']+1)*parses['page_size']]

                for video in videos:
                    res_data.append(video.data())

                return res(200, 200, "success", {"total": total, "items": res_data})
            else:
                return res(200, 200, "success", {"total": 0, "items": []})
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
