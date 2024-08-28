from app.api.models.users import UserModel


def list_sha(parser) -> dict:
    parser.add_argument("user_id", type=str, required=True, location='args')
    parser.add_argument("page_num", type=int, required=True, location='args')
    parser.add_argument("page_size", type=int, required=True, location='args')
    parses = parser.parse_args()

    if not parses['user_id']:
        raise ValueError('用户id不能为空')
    if parses['page_num'] is None:
        raise ValueError('页码不能为空')
    if parses['page_size'] is None:
        raise ValueError('单页尺寸不能为空')
    if parses['page_num'] < 0:
        raise ValueError('页码必须大于等于0')
    if parses['page_size'] <= 0:
        raise ValueError('单页尺寸必须大于0')
    if UserModel.find_by_uid(parses['user_id']) is None:
        raise ValueError('该用户不存在')

    return parses
