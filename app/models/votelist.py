from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.models.base import Base, db, MixinJSONSerializer




class Votelist(Base):
    vl_id = Column(Integer, primary_key=True)
    name = Column(String(100),comment='投票名称')
    year = Column(Integer,comment='投票年限')
    # voterstring = Column(String(200),comment='投票人字符串')
    votetype = Column(SmallInteger,comment='投票类型，1为毕业和是否授予学位的表，2为优秀毕业生表')
    votestatus = Column(SmallInteger,comment='投票状态，区别于status，status为删除使用，votestatus判断结束状态')
    votenum = Column(Integer,comment='投票人总数')

    @staticmethod
    def add_votelist(name, year, votetype,votestatus,votenum):
        with db.auto_commit():
            votelist = Votelist()
            votelist.name = name
            votelist.year = year
            votelist.votetype = votetype
            votelist.votestatus = votestatus
            votelist.votenum = votenum
            db.session.add(votelist)