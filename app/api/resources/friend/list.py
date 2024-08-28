from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.models import r
from app.api.models.users import UserModel
from app.api.schema.friend.list_sha import list_sha
from app.api.utils.res import res


class FriendList(Resource):
    @jwt_required()
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parses = list_sha(parser)

            current_user = UserModel.find_by_username(get_jwt_identity())
            list_uid = [uid.decode("utf-8") for uid in r.smembers(str(current_user.uid) + ":friends")]
            total = len(list_uid)
            if total == 0:
                return res(200, 200, "success", {"total": 0, "items": []})

            list_user = []
            if parses['page_size'] and parses['page_num']:
                if parses['page_size'] * (parses['page_num'] + 1) > total:
                    parses['page_num'] = total // parses['page_size'] - 1
                    if total % parses['page_size'] != 0:
                        parses['page_num'] += 1
                list_user = UserModel.find_by_uids(list_uid, parses['page_num'], parses['page_size'])
            else:
                list_user = UserModel.find_by_uids(list_uid)

            res_data = []
            for user in list_user:
                res_data.append(user.data())
            return res(200, 200, "success", {"total": total, "items": res_data})
        except ValueError as e:
            return res(422, 200, str(e))
        except Exception as e:
            return res(500, 500, str(e))
