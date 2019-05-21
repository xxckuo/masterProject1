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

    if int(jsonData['type']) ==1:
        results = db.session.query(Excellentresult.s_id,Excellentresult.agreenum,Excellentresult.disagreenum,Excellentresult.abstained,
                         Masterstudents.name,Masterstudents.account,Masterstudents.major,Masterstudents.title,Masterstudents.tutor,
                         Masterstudents.college,Masterstudents.thesisurl
                         ).filter(Excellentresult.s_id==Masterstudents.s_id,Excellentresult.vl_id==jsonData['vl_id']
                         ).filter(Excellentresult.agreenum>(Excellentresult.agreenum+Excellentresult.disagreenum+Excellentresult.abstained)*2/3).all()
        list = []
        for re in results:
            result={}
            result['name'] = jsonData['name']
            result['Excellentresult.s_id'] = re[0]
            result['Excellentresult.agreenum'] = re[1]
            result['Excellentresult.disagreenum'] = re[2]
            result['Excellentresult.abstained'] = re[3]
            result['Masterstudents.name'] = re[4]
            result['Masterstudents.account'] = re[5]
            result['Masterstudents.major'] = re[6]
            result['Masterstudents.title'] = re[7]
            result['Masterstudents.tutor'] = re[8]
            result['Masterstudents.college'] = re[9]
            result['Masterstudents.thesisurl'] = re[10]
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
            result['Gradusteresult.s_id'] = re[0]
            result['Graduateresult.g_agreenum'] = re[1]
            result['Graduateresult.g_disagreenum'] = re[2]
            result['Graduateresult.g_abstained'] = re[3]
            result['Graduateresult.d_agreenum'] = re[4]
            result['Graduateresult.d_disagreenum'] = re[5]
            result['Graduateresult.d_abstained'] = re[6]
            result['Masterstudents.name'] = re[7]
            result['Masterstudents.account'] = re[8]
            result['Masterstudents.major'] = re[9]
            result['Masterstudents.title'] = re[10]
            result['Masterstudents.tutor'] = re[11]
            result['Masterstudents.college'] = re[12]
            result['Masterstudents.thesisurl'] = re[13]
            list.append(result)


    return Success(msg='投票结果显示成功', data = list)