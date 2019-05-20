from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.models.base import Base, db, MixinJSONSerializer




class Graduateresult(Base):
    gr_id = Column(Integer, primary_key=True)
    s_id = Column(Integer, comment='被投票的学生的id')
    vl_id = Column(Integer,comment='参与的投票id')
    g_agreenum = Column(Integer,comment='毕业同意数量')
    g_disagreenum = Column(Integer,comment='毕业不同意数量')
    g_abstained = Column(Integer,comment='毕业弃权数量')
    d_agreenum = Column(Integer, comment='授予学位同意数量')
    d_disagreenum = Column(Integer, comment='授予学位不同意数量')
    d_abstained = Column(Integer, comment='授予学位弃权数量')