from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

class Voter(Base):
    id = Column(Integer, primary_key=True)
    teacher_account = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24))
    auth = Column(SmallInteger, default=1)#2是可以查看成绩的高级管理员1是参与投票的普通老师
    _password = Column('password', String(100))

    def keys(self):
        return ['id', 'teacher_account', 'nickname', 'auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        # self._password = generate_password_hash(raw)
        self._password = raw

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = Voter()
            user.nickname = nickname
            user.teacher_account = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(teacher_account, password):
        user = Voter.query.filter_by(teacher_account=teacher_account).first_or_404('账号不存在')
        if not user.check_password(password):
            raise AuthFailed()
        # scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        # scope = 'CmsScope' if user.auth == 2 else 'TestScope'
        if user.auth == 1:
            scope = 'UserScope'
        elif user.auth == 2:
            scope = 'AdminScope'
        elif user.auth == 3:
            scope = 'CmsScope'

        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        # return check_password_hash(self._password, raw)
        return self._password == raw

    # def _set_fields(self):
    #     # self._exclude = ['_password']
    #     self._fields = ['_password', 'nickname']
