from app.api.models.users import UserModel


def follow_list_sha(parser) -> dict:
    parser.add_argument("user_id", type=str, required=True, location="args")
    parser.add_argument("page_num", type=int, required=False, location="args")
    parser.add_argument("page_size", type=int, required=False, location="args")
    parses = parser.parse_args()

    if not parses['user_id'].strip():
        raise ValueError("用户id不能为空")
    try:
        int(parses['user_id'])
    except ValueError:
        raise ValueError("用户id错误")
    if not UserModel.find_by_uid(int(parses['user_id'])):
        raise ValueError("该用户不存在")

    return parses
