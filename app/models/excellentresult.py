from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.models.base import Base, db, MixinJSONSerializer




class Excellentresult(Base):
    er_id = Column(Integer, primary_key=True)
    s_id = Column(Integer, comment='被投票的学生的id')
    vl_id = Column(Integer,comment='参与的投票id')
    agreenum = Column(Integer,comment='同意数量')
    disagreenum = Column(Integer,comment='不同意数量')
    abstained = Column(Integer,comment='弃权数量')