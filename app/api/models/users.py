from app.config import SERVER_URL
from app.api.models import db


# 用户类
class UserModel(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.String(255), primary_key=True, nullable=False, doc="uid")  # 用户ID
    username = db.Column(db.String(20), nullable=False, doc="username")  # 用户名
    password = db.Column(db.String(255), nullable=False, doc="password")  # 用户密码
    salt = db.Column(db.String(255), nullable=False, doc="salt")  # 盐值
    avatar_url = db.Column(db.Text, nullable=False, doc="image")  # 用户头像名称

    created_at = db.Column(db.DateTime, nullable=False, doc="created_at")  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, doc="updated_at")  # 修改时间
    deleted_at = db.Column(db.DateTime, nullable=True, doc="deleted_at")  # 删除时间

    videos = db.relationship("Videos", backref="users", lazy="dynamic")

    # 添加用户
    def add_user(self):
        db.session.add(self)
        db.session.commit()

    # 获取用户信息
    def data(self):
        return {
            "id": str(self.uid),
            "username": self.username,
            "avatar_url": SERVER_URL + '/user/images/' + self.avatar_url,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "deleted_at": self.deleted_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    # 获取密码
    def get_pwd(self):
        return {
            "pwd": self.password,
            "salt": self.salt,
        }

    # 修改头像
    def update_avatar(self, avatar_name):
        self.avatar_url = avatar_name
        db.session.commit()

    # 通过用户名获取用户
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # 通过uid获取用户
    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=int(uid)).first()

    @classmethod
    def find_by_uids(cls, uids: list, page_num: int = None, page_size: int = None):
        if page_num is None:
            return db.session.query(cls).filter(cls.uid.in_(uids)).all()
        else:
            return db.session.query(cls).filter(cls.uid.in_(uids)).paginate(page=page_num+1, per_page=page_size).items
