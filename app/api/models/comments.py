from sqlalchemy import func
from ..models import db, r


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, doc="id")  # 评论的id
    parent_id = db.Column(db.Integer, nullable=False, doc="parent_id")  # 上一级评论的id
    content = db.Column(db.Text, nullable=False, doc="content")  # 评论内容
    video_id = db.Column(db.Integer, nullable=False, doc="video_id")  # 文章的id

    created_at = db.Column(db.DateTime, nullable=False, doc="created_at")  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, doc="updated_at")  # 修改时间
    deleted_at = db.Column(db.DateTime, nullable=False, doc="deleted_at")  # 删除时间

    user_id = db.Column(db.BigInteger, nullable=False, doc="user_id")  # 用户id

    # 返回评论信息
    def data(self):
        return {"id": str(self.id),
                "content": self.content,
                "video_id": str(self.video_id),
                "parent_id": str(self.parent_id),
                "user_id": str(self.user_id),
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "deleted_at": self.deleted_at,
                "like_count": int(r.hget("comments:" + str(self.id), "like_count").decode("utf-8")),
                "child_count": int(r.hget("comments:" + str(self.id), "child_count").decode("utf-8"))
                }

    # 添加评论
    def add_comment(self):
        db.session.add(self)
        db.session.commit()

    # 删除评论
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # 根据视频id删除评论
    @classmethod
    def delete_by_vid(cls, video_id):
        comments = db.session.query(cls).filter(cls.video_id == video_id).all()
        for comment in comments:
            r.delete('comments:' + str(comment.id))
            comment.delete()

        db.session.commit()

    @classmethod
    def max_id(cls):
        mid = db.session.query(func.max(cls.id)).scalar()
        return mid if mid is not None else 0

    # 根据评论id查询
    @classmethod
    def get_by_cid(cls, cid: int):
        return db.session.query(cls).filter(cls.id == cid).first()

    # 根据视频id查询
    @classmethod
    def get_by_vid(cls, vid: int, page_size: int = None, page_num: int = None):
        comments = db.session.query(cls).filter(cls.video_id == vid)
        if page_size and page_num:
            len_comments = comments.count()
            if page_size * page_num > len_comments:
                last_page = len_comments // page_size
                if len_comments % page_size != 0:
                    last_page += 1
                return comments.paginate(page=last_page, per_page=page_size).items
            else:
                return comments.paginate(page=page_num, per_page=page_size).items
        else:
            return comments.all()

    # 根据评论id查询
    @classmethod
    def get_by_parent_cid(cls, cid):
        return db.session.query(cls).filter(cls.parent_id == cid).all()
