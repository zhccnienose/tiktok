from app.api.models.videos import Videos
from app.api.models.comments import CommentModel


def publish_sha(parser) -> dict:
    parser.add_argument('video_id', type=str, required=False, default='', location='form')
    parser.add_argument('comment_id', type=str, required=False, location='form')
    parser.add_argument('content', type=str, required=True, location='form')

    parses = parser.parse_args()

    if not parses['content'].strip():
        raise ValueError('评论内容不能为空或全为空白字符')

    if not parses['video_id'] and not parses['comment_id']:
        raise ValueError('视频id和评论id不能同时为空')
    if parses['video_id'] and not Videos.get_by_vid(parses['video_id']):
        raise ValueError('该视频不存在')
    if not parses['video_id'] or (parses['comment_id'] and parses['comment_id'] and parses['comment_id'] != '0'):
        if not CommentModel.get_by_cid(parses['comment_id']):
            raise ValueError('该评论不存在')

    return parses
