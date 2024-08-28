import imghdr
from werkzeug.datastructures import FileStorage


def avatarupload_sha(parser):
    parser.add_argument('data', type=FileStorage, required=True, location='files')
    data = parser.parse_args()

    if imghdr.what(data['data']):
        return data
    else:
        raise ValueError("文件错误")
