from app.api.models.users import UserModel


def register_sha(parser) -> dict:
    """
    注册参数验证
    :param parser:参数对象
    :return: dict: ata:参数数据
    """
    # 用户名
    parser.add_argument('username', type=str, required=True, location='form')
    # 密码
    parser.add_argument('password', type=str, required=True, location='form')
    data = parser.parse_args()

    # 校验用户名
    if len(data['username'].strip()) == 0:
        raise ValueError("用户名为空")
    if UserModel.find_by_username(data['username']):
        raise ValueError("该用户名已被使用")
    # 校验密码
    if len(data['password']) == 0:
        raise ValueError("密码为空")
    if len(data['password']) > 30:
        raise ValueError("密码长度不能超过30个字符")

    return data
