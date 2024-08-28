from app.api.models.videos import Videos
from app.api.models.comments import CommentModel


def action_sha(parser) -> dict:
    """
    点赞参数校验
    :param parser:
    :return:
    """
    parser.add_argument('video_id', type=str, help='video_id', required=False, default='', location='form')
    parser.add_argument('comment_id', type=str, help='comment_id', required=False, default='', location='form')
    parser.add_argument('action_type', type=str, help='action_type', required=True, location='form')
    parses = parser.parse_args()

    if not parses['video_id'].strip() and not parses['comment_id'].strip():
        raise ValueError('视频id与评论id均为空')
    if parses['video_id'].strip() and Videos.get_by_vid(int(parses['video_id'])) is None:
        raise ValueError('该视频不存在')
    if parses['comment_id'].strip() and CommentModel.get_by_cid(int(parses['comment_id'])) is None:
        raise ValueError('该评论不存在')

    if parses['action_type'] != '1' and parses['action_type'] != '2':
        raise ValueError('操作类型错误')

    return parses
