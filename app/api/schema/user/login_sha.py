from pyotp import HOTP
from werkzeug.security import check_password_hash
from app.api.models import r
from app.api.models.users import UserModel


def login_sha(parser) -> dict:
    """
    登录参数校验
    :param parser:参数对象
    :return: dict: avatar: 登录参数
    """
    parser.add_argument('username', type=str, required=True, help="邮箱错误", location='form')
    parser.add_argument('password', type=str, required=True, help="密码错误", location='form')
    parser.add_argument('code', type=str, required=False, default="", help="校验码错误", location='form')
    data = parser.parse_args()

    if not data['username'].strip():
        raise ValueError("用户名不能为空")

    if not data['password'].strip():
        raise ValueError("密码不能为空")

    user = UserModel.find_by_username(data['username'])
    if not user:
        raise ValueError("该用户不存在")

    password, salt = user.get_pwd().get("pwd"), user.get_pwd().get("salt")
    vaild = check_password_hash(password, "{}{}".format(salt, data['password']))
    if not vaild:
        raise ValueError("密码错误")

    if r.sismember("mfa", user.uid) and not data['code'].strip():
        raise ValueError("校验码不能为空")
    if r.sismember("mfa", user.uid):
        hotp = HOTP(r.get(str(user.uid) + ":secret").decode("utf-8"))
        if not hotp.verify(data["code"], int(r.get(str(user.uid) + ":login_num").decode("utf-8"))):
            raise ValueError("校验码错误")
    return data
