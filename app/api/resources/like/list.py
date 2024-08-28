from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.videos import Videos
from app.api.models.users import UserModel
from app.api.utils.res import res

from app.api.schema.like.list_sha import list_sha


class LikeList(Resource):
    @jwt_required()
    def get(self):
        try:
            user = UserModel.find_by_username(get_jwt_identity())
            parser = reqparse.RequestParser()
            parses = list_sha(parser, str(user.uid))

            list_like = [int(vid.decode("utf-8")) for vid in r.smembers(parses['user_id'] + ":video_likes")]
            total = len(list_like)
            videos = []
            if parses['page_size'] and parses['page_num']:
                # 页码超出范围
                if parses['page_num'] * parses['page_size'] > total:
                    parses['page_num'] = total // parses['page_size']
                    if total % parses['page_size']:
                        parses['page_num'] += 1
                videos = Videos.get_by_vids(vids=list_like, page_size=parses['page_size'], page_num=parses['page_num'])
            else:
                videos = Videos.get_by_vids(vids=list_like)
            res_data = []
            for video in videos:
                res_data.append(video.data())

            return res(200, 200, "success", data={"items": res_data})
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
