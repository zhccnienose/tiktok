import pyotp
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.users import UserModel
from app.api.schema.bind_sha import bind_sha
from app.api.utils.res import res


class MfaBind(Resource):
    @jwt_required(optional=True)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            data = bind_sha(parser)
            current_user = UserModel.find_by_username(get_jwt_identity())
            if pyotp.HOTP(data['secret']).verify(data['code'],0):
                r.sadd("mfa", current_user.uid)
                r.set(str(current_user.uid)+":secret", data['secret'])
                r.set(str(current_user.uid)+":login_num", 0)
                return res(200, 200, "绑定成功")
            else:
                print("vcode:",pyotp.TOTP(data['secret']).now())
                raise ValueError("校验码错误")
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 200, str(e))
