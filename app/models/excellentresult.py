from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.models.base import Base, db, MixinJSONSerializer




class Excellentresult(Base):
    er_id = Column(Integer, primary_key=True)
    s_id = Column(Integer, comment='被投票的学生的id')
    vl_id = Column(Integer,comment='参与的投票id')
    agreenum = Column(Integer,comment='同意数量')
    disagreenum = Column(Integer,comment='不同意数量')
    abstained = Column(Integer,comment='弃权数量')

    @staticmethod
    def add_result_to_excellent(s_id, vl_id,agreenum,disagreenum,abstained):
        with db.auto_commit():
            excres = Excellentresult()
            excres.s_id = s_id
            excres.vl_id = vl_id
            excres.agreenum = agreenum
            excres.disagreenum = disagreenum
            excres.abstained = abstained
            db.session.add(excres)