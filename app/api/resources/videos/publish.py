import os
import cv2
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.schema.video.video_sha import video_sha
from app.api.utils.res import res
from app.api.models import r
from app.api.models.videos import Videos
from app.api.models.users import UserModel
from app.config import VIDEO_PATH, COVER_PATH


class VideoPublish(Resource):
    # 添加视频
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            data = video_sha(parser)

            num = Videos.max_id() + 1
            # 用户信息
            uid = UserModel.find_by_username(get_jwt_identity()).data()['id']
            data['uid'] = uid
            # 保存视频文件
            video_name = f"{str(num)}_{str(uid)}.{data['data'].content_type.split('/')[1]}"
            data['filename'] = video_name
            path = os.path.join(VIDEO_PATH, video_name)
            data['data'].save(path)

            # 封面
            video_file = cv2.VideoCapture(path)
            flag, frame = video_file.read()
            if flag:
                cover_name = f"{str(num)}_{str(uid)}.jpg"
                cover_path = os.path.join(COVER_PATH, cover_name)
                cv2.imwrite(cover_path, frame)
                video_file.release()
                cv2.destroyAllWindows()

            # 时间
            data['created_at'] = datetime.now()
            data['updated_at'] = datetime.now()
            # 初始化为过去一年的时间
            data['deleted_at'] = datetime.now() - timedelta(days=365)

            # redis中添加相关数据,点赞数，评论数，点击数收藏数
            r.hmset(str(num) + '_' + str(uid), {"likes": 0, "comments": 0, "visits": 0})
            r.zadd("list_hot", {str(num) + '_' + str(uid): 0})
            # 添加视频
            vid = Videos(**data)
            vid.add()

            return res(200, 200, "success")
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
