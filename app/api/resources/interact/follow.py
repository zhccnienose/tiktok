from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.users import UserModel
from app.api.schema.interact.follow_sha import follow_sha
from app.api.utils.res import res


class Follow(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parses = follow_sha(parser)

            current_user = UserModel.find_by_username(get_jwt_identity())
            msg = ""
            # 关注操作
            if not parses['action_type']:
                if not r.sismember(str(current_user.uid) + ":set_follows", parses['to_user_id']):
                    r.hincrby(parses['to_user_id'], "fan_nums", 1)
                    r.hincrby(current_user.uid, "follow_nums", 1)
                    r.sadd(str(current_user.uid) + ":set_follows", parses['to_user_id'])
                    r.sadd(parses['to_user_id'] + ":set_fans", current_user.uid)
                    msg = "关注成功"
                else:
                    raise ValueError("该用户已在关注列表中")
            # 取消关注操作
            else:
                if r.sismember(str(current_user.uid) + ":set_follows", parses['to_user_id']):
                    r.hincrby(parses['to_user_id'], "fan_nums", -1)
                    r.hincrby(current_user.uid, "follow_nums", -1)
                    r.srem(str(current_user.uid) + ":set_follows", parses['to_user_id'])
                    r.srem(parses['to_user_id'] + ":set_fans", current_user.uid)
                    msg = "取消关注成功"
                else:
                    raise ValueError("该用户不在关注列表中")
            return res(200, 200, msg)
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
