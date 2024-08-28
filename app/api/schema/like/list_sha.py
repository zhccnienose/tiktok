from app.api.models.users import UserModel


def list_sha(parser,current_id) -> dict:
    parser.add_argument('user_id', type=str, required=False, help='user_id error', default=current_id, location='args')
    parser.add_argument('page_size', type=int, required=False, help='page_size error', location='args')
    parser.add_argument('page_num', type=int, required=False, help='page_num error', location='args')
    parses = parser.parse_args()

    # print(parses['user_id'])
    if parses['user_id'] and not UserModel.find_by_uid(parses['user_id']):
        raise ValueError("该用户不存在")
    if parses['page_size'] is not None and parses['page_size'] <= 0:
        raise ValueError("每页数据量错误")
    if parses['page_num'] is not None and parses['page_num'] < 0:
        raise ValueError("页码错误")
    return parses
