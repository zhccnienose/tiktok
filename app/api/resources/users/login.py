import pyotp
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token


from app.api.schema.user.login_sha import login_sha
from app.api.models import r
from app.api.models.users import UserModel
from app.api.utils.res import res


# 用户登录
class UserLogin(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            data = login_sha(parser)

            user = UserModel.find_by_username(data['username'])

            # 登录次数+1
            r.incrby(str(user.uid) + ":login_num", 1)
            tokens = generate_token(data['username'])
            data = user.data()
            data["tokens"] = tokens

            return res(status=200, code=200, msg="success", data=data)
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(status=500, code=500, msg=str(e))


def generate_token(username):
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return {
        'access_token': 'Bearer ' + access_token,
        'refresh_token': 'Bearer ' + refresh_token,
    }
