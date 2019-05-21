from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.libs.error_code import Success
from app.models.base import Base, db, MixinJSONSerializer

class Voterin(Base):
    vi_id = Column(Integer, primary_key=True)
    vl_id = Column(Integer,comment='参与的投票id')
    voter_id = Column(Integer,comment='参与的投票人id')
    voterinstatus = Column(SmallInteger,comment='判断是否已完成投票',default=0)

    @staticmethod
    def add_voter_to_voterin(vl_id, voter_id):
        with db.auto_commit():
            voterin = Voterin()
            voterin.vl_id = vl_id
            voterin.voter_id = voter_id
            # voterin.voterinstatus = secret
            db.session.add(voterin)

    @staticmethod
    def update_voter_status(vl_id, voter_id):
        with db.auto_commit():
            voterin = Voterin.query.filter(Voterin.vl_id == vl_id, Voterin.voter_id == voter_id).first_or_404('您未参与该投票，请联系管理员')
            if voterin.voterinstatus == 1:
                # 校验是否重复投票
                raise Success(msg='您已投过票，请勿重复投票')
            voterin.voterinstatus = 1

    @staticmethod
    def check_vote_and_update_status(vl_id):
        # 检查是否是最后一个人投票，如果是，则更新投票列表状态
        with db.auto_commit():
            voteres = Voterin.query.filter(Voterin.vl_id == vl_id,Voterin.voterinstatus == 0).first()
            if voteres:
                return False
            return True