from app.api.models.videos import Videos
from app.api.models.comments import CommentModel


def delete_sha(parser) -> dict:
    parser.add_argument('video_id', type=str, required=False, default='', location='form')
    parser.add_argument('comment_id', type=str, required=False, default='', location='form')
    parses = parser.parse_args()
    parses['video_id'] = parses['video_id'].strip()
    parses['comment_id'] = parses['comment_id'].strip()

    if not parses['video_id'] and not parses['comment_id']:
        raise ValueError("视频id和评论id不能同时为空")
    try:
        if parses['video_id'] and not Videos.get_by_vid(int(parses['video_id'])):
            raise ValueError("视频id错误")
    except ValueError:
        raise ValueError("视频id错误")
    try:
        if parses['comment_id'] and not CommentModel.get_by_cid(int(parses['comment_id'])):
            raise ValueError("评论id错误")
    except ValueError:
        raise ValueError("评论id错误")

    return parses
