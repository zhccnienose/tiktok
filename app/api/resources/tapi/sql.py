from flask import jsonify
from flask_restful import Resource
from app.api.models.users import UserModel


class TestSql(Resource):
    def get(self):
        list_user = UserModel.get_all_user()
        data = []
        for user in list_user:
            data.append(user.data())
        return jsonify(code=200, data={"userlist": data})
