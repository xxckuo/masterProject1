from flask import  request
from app.libs.error_code import  Success
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.masterstudents import Masterstudents


api = Redprint('getmessages')
@api.route('/getmessages',methods = ['POST'])
def getmessages():
    jsonData = request.get_json()
    if jsonData['votetype']== 1:
        a = db.session.query(Excellentresult.s_id,Excellentresult.agreenum,Excellentresult.disagreenum,Excellentresult.abstained,Masterstudents.s_id,Masterstudents.account,Masterstudents.major,Masterstudents.title,Masterstudents.tutor,Masterstudents.college,Masterstudents.thesisurl,Masterstudents.name).join(Excellentresult,Excellentresult.s_id==Masterstudents.s_id).filter(Excellentresult.vl_id == jsonData['vl_id']).all()
        # b= db.session.query(Excellentresult.s_id,Excellentresult.agreenum,Excellentresult.disagreenum,Excellentresult.abstained,Voterin.voterinstatus,Voter.nickname,Voter.teacher_account,Voter.auth,Votelist.votestatus,Votelist.votenum).join(Voterin,Voterin.voter_id == Voter.id).filter(Voterin.vl_id == jsonData['vl_id'],Votelist.vl_id==jsonData['vl_id'],Excellentresult.vl_id==jsonData['vl_id']).all()
        messages = []
        for t in a:
            d = {}
            d['s_id'] = t[0]
            d['agreenum'] = 0
            d['disagreenum'] = 0
            d['abstained'] = 0
            d['student_account'] = t[4]
            d['student_major'] = t[5]
            d['student_title'] = t[6]
            d['student_tutor'] = t[7]
            d['student_league'] = t[8]
            d['team_name'] = t[9]
            d['thesisurl'] = t[10]
            d['student_name'] = t[10]
            messages.append(d)

    if jsonData['votetype'] == 2:
        a = db.session.query(Graduateresult.s_id, Graduateresult.g_agreenum,Graduateresult.g_disagreenum,Graduateresult.g_abstained,
                             Graduateresult.d_agreenum, Graduateresult.d_disagreenum,Graduateresult.d_abstained,Masterstudents.s_id, Masterstudents.account,
                             Masterstudents.major, Masterstudents.title, Masterstudents.tutor,
                             Masterstudents.college, Masterstudents.thesisurl,Masterstudents.name).join(Graduateresult,
                                                                                    Graduateresult.s_id == Masterstudents.s_id).filter(
            Graduateresult.vl_id == jsonData['vl_id']).all()
        # b= db.session.query(Excellentresult.s_id,Excellentresult.agreenum,Excellentresult.disagreenum,Excellentresult.abstained,Voterin.voterinstatus,Voter.nickname,Voter.teacher_account,Voter.auth,Votelist.votestatus,Votelist.votenum).join(Voterin,Voterin.voter_id == Voter.id).filter(Voterin.vl_id == jsonData['vl_id'],Votelist.vl_id==jsonData['vl_id'],Excellentresult.vl_id==jsonData['vl_id']).all()
        messages = []
        for t in a:
            d = {}
            d['s_id'] = t[0]
            d['g_agreenum'] = 0
            d['g_disagreenum'] = 0
            d['g_abstained'] = 0
            d['d_agreenum'] =0
            d['d_disagreenum'] = 0
            d['d_abstained'] = 0
            d['student_account'] = t[7]
            d['student_major'] = t[8]
            d['student_title'] = t[9]
            d['student_tutor'] = t[10]
            d['student_league'] = t[11]
            d['team_name'] = t[12]
            d['thesisurl'] = t[13]
            d['student_name'] = t[14]
            messages.append(d)

    return Success(msg='投票结果显示成功',data=messages)