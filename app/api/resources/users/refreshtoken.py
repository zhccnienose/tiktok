from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from app.api.utils.res import res


class RefreshToken(Resource):

    @jwt_required(refresh=True)
    def get(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return res(code=200, msg="success", data={"access_token": access_token})
