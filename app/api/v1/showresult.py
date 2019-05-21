import fractions

from flask import  request
from app.libs.error_code import  Success
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.masterstudents import Masterstudents

api = Redprint('show_result')

@api.route('/show',methods=['POST'])
def add_students():
    jsonData = request.get_json()
    x = fractions.Fraction(2, 3)

    # 是否需要在全部完成投票后形成汇总
    # 分页？
    # 判断投票是否已结束，根据votestatus进行判断
    if int(jsonData['type']) ==1:
        results = db.session.query(Excellentresult.s_id,Excellentresult.agreenum,Excellentresult.disagreenum,Excellentresult.abstained,
                         Masterstudents.name,Masterstudents.account,Masterstudents.major,Masterstudents.title,Masterstudents.tutor,
                         Masterstudents.college,Masterstudents.thesisurl
                         ).filter(Excellentresult.s_id==Masterstudents.s_id,Excellentresult.vl_id==jsonData['vl_id'],).all()

        list = []
        for re in results:
            result={}

            result['name'] = jsonData['name']
            result['s_id'] = re[0]
            result['agreenum'] = re[1]
            result['disagreenum'] = re[2]
            result['abstained'] = re[3]
            result['name'] = re[4]
            result['account'] = re[5]
            result['major'] = re[6]
            result['title'] = re[7]
            result['tutor'] = re[8]
            result['college'] = re[9]
            result['thesisurl'] = re[10]
            result['pass'] = 0

            if re[1]>(re[1]+re[2]+re[3])*x:
                result['pass'] = 1
            else:
                result['pass'] = 0
            list.append(result)


    else :
        results = db.session.query(Graduateresult.s_id,Graduateresult.g_agreenum,Graduateresult.g_disagreenum,Graduateresult.g_abstained,
                                   Graduateresult.d_agreenum, Graduateresult.d_disagreenum, Graduateresult.d_abstained,
                         Masterstudents.name,Masterstudents.account,Masterstudents.major,Masterstudents.title,Masterstudents.tutor,
                         Masterstudents.college,Masterstudents.thesisurl
                         ).filter(Graduateresult.s_id==Masterstudents.s_id,Graduateresult.vl_id==jsonData['vl_id']
                         ).all()
        list=[]
        for re in results:
            result = {}
            result['name'] = jsonData['name']
            result['s_id'] = re[0]
            result['g_agreenum'] = re[1]
            result['g_disagreenum'] = re[2]
            result['g_abstained'] = re[3]
            result['d_agreenum'] = re[4]
            result['d_disagreenum'] = re[5]
            result['d_abstained'] = re[6]
            result['name'] = re[7]
            result['account'] = re[8]
            result['major'] = re[9]
            result['title'] = re[10]
            result['tutor'] = re[11]
            result['college'] = re[12]
            result['thesisurl'] = re[13]
            list.append(result)


    return Success(msg='投票结果显示成功', data = list)