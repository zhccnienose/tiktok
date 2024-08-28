def list_sha(parser) -> dict:
    parser.add_argument("page_size", type=int, required=False, location='args')
    parser.add_argument("page_num", type=int, required=False, location='args')

    parses = parser.parse_args()

    if parses['page_size'] and parses['page_size'] <= 0:
        raise ValueError("每页记录数必须大于0")
    if parses['page_num'] and parses['page_num'] < 0:
        raise ValueError("页码必须大于等于0")

    return parses
