from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.models.base import Base, db, MixinJSONSerializer




class Votelist(Base):
    vl_id = Column(Integer, primary_key=True)
    name = Column(String(100),comment='投票名称')
    year = Column(Integer,comment='投票年限')
    # voterstring = Column(String(200),comment='投票人字符串')
    votetype = Column(SmallInteger,comment='投票类型，1为毕业和是否授予学位的表(长)，2为优秀毕业生表（短）')
    votestatus = Column(SmallInteger,comment='投票状态，区别于status，status为删除使用，votestatus判断结束状态')
    votenum = Column(Integer,comment='投票人总数')

    def keys(self):
        return ['vl_id','name', 'year', 'votetype', 'votestatus','votenum','create_time']

    @staticmethod
    def add_votelist(name, year, votetype, votestatus, votenum):
        with db.auto_commit():
            votelist = Votelist()
            votelist.name = name
            votelist.year = year
            votelist.votetype = votetype
            votelist.votestatus = votestatus
            votelist.votenum = votenum
            db.session.add(votelist)

    @staticmethod
    def update_votelist_status(vl_id):
        with db.auto_commit():
            vote = Votelist.query.filter(Votelist.vl_id == vl_id).first()
            vote.votestatus = 1

    @staticmethod
    def update_votelist(data):
        with db.auto_commit():
            vote = Votelist.query.filter(Votelist.vl_id == data['vl_id']).first()
            if data['name'] != '':
                print('不空')
                vote.name = data['name']
            if data['year'] != '':
                vote.year = data['year']
            if data['votetype'] != '':
                vote.votetype = data['votetype']
            if data['votestatus'] != '':
                vote.votestatus = data['votestatus']
            if data['votenum'] != '':
                vote.votenum = data['votenum']