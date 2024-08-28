from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.users import UserModel
from app.api.schema.friend.action_sha import action_sha
from app.api.utils.res import res


class FirendAction(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parses = action_sha(parser)
            current_user = UserModel.find_by_username(get_jwt_identity())
            list_friend = [uid.decode("utf-8") for uid in r.smembers(str(current_user.uid) + ":friends")]

            if parses['user_id'] in list_friend:
                raise ValueError("已添加该用户为好友")
            else:
                r.sadd(str(current_user.uid) + ":friends", parses['user_id'])
                r.sadd(parses['user_id'] + ":friends", current_user.uid)
            return res(200, 200, "添加好友成功")
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
