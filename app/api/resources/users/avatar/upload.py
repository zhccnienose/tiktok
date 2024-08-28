import imghdr
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.models.users import UserModel
from app.config import IMAGE_PATH
from app.api.utils.res import res
from app.api.schema.user.avatarupload_sha import avatarupload_sha


# 修改头像
class UserAvatarUpload(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            data = avatarupload_sha(parser)

            current_user = UserModel.find_by_username(get_jwt_identity())
            uid = current_user.uid
            imgname = str(uid) + "." + imghdr.what(data['data'])
            data['data'].save(IMAGE_PATH + imgname)
            print('------------------')
            current_user.update_avatar(imgname)
            print('------------------')
            res_data = current_user.data()
            res_data['password'] = current_user.get_pwd()['pwd']
            return res(200, 200, "success", res_data)
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
