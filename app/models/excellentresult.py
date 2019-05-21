from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm

from app.libs.error_code import Success
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

    @staticmethod
    def update_excellent_result(s_id, vl_id, excellent_result):
        with db.auto_commit():
            exce = Excellentresult.query.filter(Excellentresult.s_id == s_id,Excellentresult.vl_id == vl_id).first_or_404('该学生未参与投票'+s_id)
            exce.agreenum = exce.agreenum - 1
            if int(excellent_result) == 1:
                exce.disagreenum = exce.disagreenum + 1
            elif int(excellent_result) == 2:
                exce.abstained = exce.abstained + 1

    @staticmethod
    def update_excellent_result_by_all(s_id, vl_id, excellent_result):
        with db.auto_commit():
            exce = Excellentresult.query.filter(Excellentresult.s_id == s_id,
                                                Excellentresult.vl_id == vl_id).first_or_404('该学生未参与投票' + s_id)
            if int(excellent_result) == 1:
                exce.disagreenum = exce.disagreenum + 1
            elif int(excellent_result) == 2:
                exce.abstained = exce.abstained + 1
            elif int(excellent_result) == 0:
                exce.agreenum = exce.agreenum + 1