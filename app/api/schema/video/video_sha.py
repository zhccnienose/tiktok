import os
from werkzeug.datastructures import FileStorage


def video_sha(parser):
    parser.add_argument('title', type=str, required=False, help="title error", location='form')  # 标题
    parser.add_argument('description', type=str, required=False, help="description error", location='form')  # 简述
    parser.add_argument('data', type=FileStorage, required=True, location='files')  # 视频文件

    data = parser.parse_args()
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv', '.flv']
    extension = os.path.splitext(data['data'].filename)[-1].lower()
    if extension not in VIDEO_EXTENSIONS:
        raise ValueError("文件格式错误")

    if data['title'] is not None:
        if len(data['title']) == 0:
            raise ValueError("标题为空")
    else:
        data['title'] = "标题"
    if not data['data']:
        raise ValueError("视频不存在")
    return data
