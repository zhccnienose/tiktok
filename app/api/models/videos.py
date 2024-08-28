from datetime import datetime
from sqlalchemy import func, or_
from . import db, r
from app.config import SERVER_URL
from .users import UserModel


class Videos(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)  # 视频id
    title = db.Column(db.String(100), nullable=False, doc='title')  # 标题
    description = db.Column(db.Text, nullable=False, doc="description")  # 简介
    filename = db.Column(db.Text, nullable=False, doc="filename")  # 视频文件名

    created_at = db.Column(db.DateTime, nullable=True, doc="created_at")  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=True, doc="updated_at")  # 修改时间
    deleted_at = db.Column(db.DateTime, nullable=True, doc="deleted_at")  # 删除时间

    uid = db.Column(db.String(255), db.ForeignKey('users.uid'), nullable=False, doc="uid")  # 作者id

    # 添加视频
    def add(self):
        db.session.add(self)
        db.session.commit()

    # 获取数据
    def data(self):
        return {"id": str(self.id),
                "user_id": self.uid,
                "title": self.title,
                "description": self.description,
                "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "deleted_at": self.deleted_at.strftime("%Y-%m-%d %H:%M:%S"),
                "video_url": SERVER_URL + "/video/files/" + self.filename,
                "cover_url": SERVER_URL + "/video/covers/" + self.filename,

                "like_count": int(r.hget(str(self.id) + "_" + str(self.uid), "likes").decode("utf-8")),
                "comment_count": int(r.hget(str(self.id) + "_" + str(self.uid), "comments").decode("utf-8")),
                "visit_count": int(r.hget(str(self.id) + "_" + str(self.uid), "visits").decode("utf-8"))
                }

    # 视频数
    @classmethod
    def count(cls):
        return db.session.query(cls).count()

    @classmethod
    def max_id(cls):
        mid = db.session.query(func.max(cls.id)).scalar()
        return mid if mid is not None else 0

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    # 某时间之后的视频流
    @classmethod
    def get_by_time(cls, latest_time):
        # 时间戳转化为时间字符串
        time_str = datetime.strftime(datetime.fromtimestamp(int(latest_time)), "%Y-%m-%d %H:%M:%S")
        return db.session.query(cls).filter(cls.created_at >= time_str).all()

    # 获取用户的发布列表
    @classmethod
    def get_by_uid(cls, uid):
        return db.session.query(cls).filter(cls.uid == uid).all()

    # 获取用户的发布列表
    @classmethod
    def get_by_vid(cls, vid: int):
        return db.session.query(cls).filter(cls.id == vid).first()

    @classmethod
    def get_by_vids(cls, vids: list, page_num: int = None, page_size: int = None):
        if page_num is not None and page_size is not None:
            return db.session.query(cls).filter(cls.id.in_(vids)).paginate(page=page_num + 1, per_page=page_size).items
        else:
            return db.session.query(cls).filter(cls.id.in_(vids)).all()

    # 根据关键字搜索
    @classmethod
    def get_by_keyword(cls, keywords, page_num, page_size, from_date=None, to_date=None, username=''):
        # 关键字查询
        videos = None
        if keywords:
            videos = db.session.query(cls).filter(
                or_(cls.title.like(f"%{keywords}%"), cls.description.like(f"%{keywords}%")))
        if from_date and to_date:
            # print(from_date, to_date)
            start_date = datetime.fromtimestamp(from_date)
            end_date = datetime.fromtimestamp(to_date)

            videos = videos.filter(cls.created_at.between(start_date, end_date))
        if username:
            # print(username)
            authors = UserModel.query.filter(UserModel.username.like(f"%{username}%")).all()
            if authors:
                uids = [author.uid for author in authors]
                videos = videos.filter(cls.uid.in_(uids))
            else:
                videos = []

        if videos is None:
            videos = db.session.query(cls)
        videos_list = videos.paginate(page=page_num + 1, per_page=page_size).items
        return videos_list
