from app.api.models.users import UserModel


def action_sha(parser) -> dict:
    parser.add_argument('user_id', type=str, required=True, location='args')
    parses = parser.parse_args()

    if not parses['user_id'].strip():
        raise ValueError("用户id不能为空")
    if not UserModel.find_by_uid(parses['user_id']):
        raise ValueError("该用户不存在")

    return parses
