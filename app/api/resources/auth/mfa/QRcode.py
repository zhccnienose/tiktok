import pyotp
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.api.utils.res import res
from app.api.utils.make_qrcode import make_qrcode


class MfaQRcode(Resource):
    @jwt_required(optional=True)
    def get(self):
        rand_key = pyotp.random_base32()
        code = pyotp.HOTP(rand_key).at(0)
        print("rand_key:", rand_key)
        print("code:", code)
        qrcode_base64 = make_qrcode(code)
        data = {"secret": rand_key, "qrcode": qrcode_base64}
        return res(status=200, code=200, msg="success", data=data)
