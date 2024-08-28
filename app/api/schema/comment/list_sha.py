from app.api.models.videos import Videos
from app.api.models.comments import CommentModel


def list_sha(parser) -> dict:
    parser.add_argument('video_id', type=str, required=True, default='', location='args')
    parser.add_argument('comment_id', type=str, required=True, default='', location='args')
    parser.add_argument('page_size', type=int, required=False, location='args')
    parser.add_argument('page_num', type=int, required=False, location='args')
    parses = parser.parse_args()

    if not parses['video_id'].strip() and not parses['comment_id'].strip():
        raise ValueError("视频id与评论id不能同时为空")
    if parses['video_id'].strip() and not Videos.get_by_vid(int(parses['video_id'])):
        raise ValueError("该视频不存在")
    if parses['comment_id'].strip() and not CommentModel.get_by_cid(int(parses['comment_id'])):
        raise ValueError("该评论不存在")
    if parses['page_size'] is not None and parses['page_size'] <= 0:
        raise ValueError("每页记录数必须大于0")
    if parses['page_num'] is not None and parses['page_num'] < 0:
        raise ValueError("页码必须大于等于0")

    return parses
