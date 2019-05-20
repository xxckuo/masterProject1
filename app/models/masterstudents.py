from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

class Masterstudents(Base):
    s_id = Column(Integer, primary_key=True)
    name = Column(String(24), comment='学生姓名')
    account = Column(Integer, comment='学生学号')
    major = Column(String(24),comment='学科、专业')
    title = Column(String(100),comment='论文题目')
    tutor = Column(String(20),comment='指导教师')
    college = Column(String(24),comment='所在培养单位')
    thesisurl = Column(String(500),comment='论文连接')
    _password = Column('password', String(100))

    def keys(self):
        return ['id', 'email', 'nickname', 'auth']

    @staticmethod
    def add_student(name, account, major, title, tutor,college,thesisurl):
        with db.auto_commit():
            masstu = Masterstudents()
            masstu.name = name
            masstu.account = account
            masstu.major = major
            masstu.title = title
            masstu.tutor = tutor
            masstu.college = college
            masstu.thesisurl = thesisurl
            db.session.add(masstu)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)