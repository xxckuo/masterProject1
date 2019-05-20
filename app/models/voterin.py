from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.models.base import Base, db, MixinJSONSerializer

class Voterin(Base):
    vi_id = Column(Integer, primary_key=True)
    vl_id = Column(Integer,comment='参与的投票id')
    voter_id = Column(Integer,comment='参与的投票人id')
    voterinstatus = Column(SmallInteger,comment='判断是否已完成投票',default=0)