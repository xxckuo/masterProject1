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

    @staticmethod
    def add_result_to_graduate(s_id, vl_id, g_agreenum, g_disagreenum, g_abstained,d_agreenum,d_disagreenum,d_abstained):
        with db.auto_commit():
            excres = Graduateresult()
            excres.s_id = s_id
            excres.vl_id = vl_id
            excres.g_agreenum = g_agreenum
            excres.g_disagreenum = g_disagreenum
            excres.g_abstained = g_abstained
            excres.d_agreenum = d_agreenum
            excres.d_disagreenum = d_disagreenum
            excres.d_abstained = d_abstained
            db.session.add(excres)

    @staticmethod
    def update_graduatew_result(s_id, vl_id, graduate_result,degree_result):
        with db.auto_commit():
            grad = Graduateresult.query.filter(Graduateresult.s_id == s_id,
                                               Graduateresult.vl_id == vl_id).first_or_404('该学生未参与投票'+str(s_id)
                                                                                           )
            if int(graduate_result) == 1:
                grad.g_agreenum = grad.g_agreenum - 1
                grad.g_disagreenum = grad.g_disagreenum + 1
            elif int(graduate_result) == 2:
                grad.g_agreenum = grad.g_agreenum - 1
                grad.g_abstained = grad.g_abstained + 1

            if int(degree_result) == 1:
                grad.d_agreenum = grad.d_agreenum - 1
                grad.d_disagreenum = grad.d_disagreenum + 1
            elif int(degree_result) == 2:
                grad.d_agreenum = grad.d_agreenum - 1
                grad.d_abstained = grad.d_abstained + 1

    @staticmethod
    def update_graduatew_result_by_all(gr_id, graduate_result, degree_result):
        with db.auto_commit():
            grad = Graduateresult.query.filter(Graduateresult.gr_id == gr_id).first_or_404('该学生未参与投票')


            if int(degree_result) == 1:
                grad.d_agreenum = grad.d_agreenum - 1
                grad.d_disagreenum = grad.d_disagreenum + 1
            elif int(degree_result) == 2:
                grad.d_agreenum = grad.d_agreenum - 1
                grad.d_abstained = grad.d_abstained + 1
            # elif int(degree_result) == 0:
            #     grad.d_agreenum = grad.d_agreenum + 1


            if int(graduate_result) == 1:
                grad.g_disagreenum = grad.g_disagreenum + 1
                grad.g_agreenum = grad.g_agreenum - 1
            elif int(graduate_result) == 2:
                grad.g_abstained = grad.g_abstained + 1
                grad.g_agreenum = grad.g_agreenum - 1
            # elif int(graduate_result) == 0:
            #     grad.g_agreenum = grad.g_agreenum + 1