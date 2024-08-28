def search_sha(parser) -> dict:
    parser.add_argument('keywords', type=str, required=True, location='form')
    parser.add_argument('page_size', type=int, required=True, location='form')
    parser.add_argument('page_num', type=int, required=True, location='form')

    parser.add_argument('from_date', type=int, required=False, location='form')
    parser.add_argument('to_date', type=int, required=False, location='form')
    parser.add_argument('username', type=str, required=False, location='form')
    data = parser.parse_args()
    return data
