from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.users import UserModel
from app.api.models.videos import Videos
from app.api.models.comments import CommentModel
from app.api.schema.like.action_sha import action_sha
from app.api.utils.res import res


class LikeActions(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parses = action_sha(parser)
            current_uid = UserModel.find_by_username(get_jwt_identity()).uid
            num = -1 if parses['action_type'] == '2' else 1

            if parses['video_id'].strip():
                video = Videos.get_by_vid(int(parses['video_id']))
                video_likes = [id.decode("utf-8") for id in r.smembers(str(current_uid)+":video_likes")]
                if num == 1:
                    if parses['video_id'] not in video_likes:
                        r.hincrby(parses['video_id'] + "_" + str(video.uid), "likes", 1)
                        r.sadd(str(current_uid) + ":video_likes", parses['video_id'])
                    else:
                        raise ValueError("该视频不可点赞")
                elif num == -1:
                    if parses['video_id'] in video_likes:
                        r.hincrby(parses['video_id'] + "_" + str(video.uid), "likes", -1)
                        r.srem(str(current_uid) + ":video_likes", parses['video_id'])
                    else:
                        raise ValueError("该视频不可取消点赞")
            if parses['comment_id'].strip():
                comment = CommentModel.get_by_cid(int(parses['comment_id']))
                comment_likes = [id.decode("utf-8") for id in r.smembers(str(current_uid) + ":comment_likes")]
                if num == 1:
                    if parses['comment_id'] not in comment_likes:
                        r.hincrby("comments:" + parses['comment_id'], "like_count", 1)
                        r.sadd(str(current_uid) + ":comment_likes", parses['comment_id'])
                    else:
                        raise ValueError("该评论不可点赞")
                elif num == -1:
                    if parses['comment_id'] in comment_likes:
                        r.hincrby("comments:" + parses['comment_id'], "like_count", -1)
                        r.srem(str(current_uid) + ":comment_likes", parses['comment_id'])
                    else:
                        raise ValueError("该评论不可取消点赞")

            return res(200, 200, "success")
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
