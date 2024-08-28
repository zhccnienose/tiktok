import uuid
from random import randint
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from app.api.schema.user.register_sha import register_sha
from app.api.models import r
from app.api.models.users import UserModel
from app.api.utils.res import res
from app.api.utils.snow_fake import SnowFake


class UserRegister(Resource):

    def post(self):
        try:
            parser = reqparse.RequestParser()
            data = register_sha(parser)

            snow_fake = SnowFake(1, 1)
            data['uid'] = snow_fake.next_id()
            data['salt'] = uuid.uuid4().hex
            data['password'] = generate_password_hash(f"{data['salt']}{data['password']}")

            data['avatar_url'] = str(randint(1, 6)) + ".jpg"
            data['created_at'] = datetime.now()
            data['updated_at'] = datetime.now()
            # 初始化为过去一年的时间
            data['deleted_at'] = datetime.now() - timedelta(days=365)
            user = UserModel(**data)
            user.add_user()
            # 粉丝数，关注数，评分，积分
            r.hmset(data['uid'], {"fan_nums": 0, "follow_nums": 0})

            return res(status=200, code=200, msg="注册成功")
        except ValueError as e:
            return res(status=422, code=200, msg=str(e))
        except Exception as e:
            return res(status=200, code=200, msg=str(e))
