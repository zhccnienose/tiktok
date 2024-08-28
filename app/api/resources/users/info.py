from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.api.models.users import UserModel
from app.api.utils.res import res


class UsersInfo(Resource):
    @jwt_required(optional=True)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int, required=True, location='args')
            data = parser.parse_args()

            user = UserModel.find_by_uid(data['user_id'])
            if not user:
                raise ValueError("该用户不存在")

            return res(status=200, code=200, msg="success", data=user.data())
        except ValueError as e:
            return res(422, 200, str(e), data={})
        except Exception as e:
            return res(500, 500, str(e))
