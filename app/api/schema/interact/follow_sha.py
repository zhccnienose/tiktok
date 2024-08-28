from app.api.models.users import UserModel


def follow_sha(parser) -> dict:
    parser.add_argument('to_user_id', type=str, required=True, location='form')
    parser.add_argument('action_type', type=int, required=True, location='form')
    parses = parser.parse_args()

    if parses['action_type'] != 1 and parses['action_type'] != 0:
        raise ValueError("操作类型错误")
    if not parses['to_user_id']:
        raise ValueError("操作对象用户id不能为空")
    try:
        int(parses['to_user_id'])
    except ValueError:
        raise ValueError("操作对象用户id应为数字")

    if not UserModel.find_by_uid(int(parses['to_user_id'])):
        raise ValueError("该用户不存在")

    return parses
