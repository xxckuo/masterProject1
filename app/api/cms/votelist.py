from flask import request
from sqlalchemy import func

from app.libs.error_code import Success, SuccessPage
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.masterstudents import Masterstudents
from app.models.votelist import Votelist
from app.models.voter import Voter
from app.models.voterin import Voterin


api = Redprint('votelist')

@api.route('/getvotelist')
@auth.login_required
def get():
    vls = Votelist.query.filter(Votelist.status!=0).all()
    return Success(msg='查询列表成功', data=vls)

@api.route('/createlist',methods=['POST'])
@auth.login_required
def create_list():
    jsonData = request.get_json()
    Votelist.add_votelist(jsonData['name'],jsonData['year'],jsonData['votetype'],jsonData['votestatus'],jsonData['votenum'])
    return Success(msg='新增成功',error_code=201)

@api.route('/updatevotelist',methods=['POST'])
@auth.login_required
def update_votelist():
    jsonData = request.get_json()
    Votelist.update_votelist(jsonData)
    return Success(msg='修改成功')

@api.route('/get_have_voter',methods=['POST'])
@auth.login_required
def get_voter_voterin():
    data = request.get_json()
    vl_id = request.args.get('vl_id')
    voterinres = db.session.query(Voterin.vi_id,Voterin.vl_id,Voterin.voter_id,Voterin.voterinstatus,Voter.id,
                                  Voter.teacher_account,Voter.nickname,Voter.auth).filter(Voterin.vl_id == vl_id,Voter.id == Voterin.voter_id).limit(data['limit']).offset(data['offset']).all()
    totalres = db.session.query(func.count(Voterin.vi_id)).filter(Voterin.vl_id == vl_id,Voter.id == Voterin.voter_id).first()
    voterinList = []
    for vi in voterinres:
        templist = {}
        templist['vi_id'] = vi[0]
        templist['vl_id'] = vi[1]
        templist['voter_id'] = vi[2]
        templist['voterinstatus'] = vi[3]
        templist['voter_id'] = vi[4]
        templist['teacher_account'] = vi[5]
        templist['nickname'] = vi[6]
        templist['auth'] = vi[7]
        voterinList.append(templist)
    return SuccessPage(data=voterinList,totalnum=totalres[0])

@api.route('/get_havet_voter')
@auth.login_required
def get_all_voter():
    vl_id = request.args.get('vl_id')
    voterinres = db.session.query(Voterin.voter_id).filter(Voterin.vl_id == vl_id).all()
    voterHaveInList = []
    for vi in voterinres:
        voterHaveInList.append(vi[0])
    voterlist = Voter.query.filter(Voter.id.notin_(voterHaveInList),Voter.auth!=3).all()
    return Success(data=voterlist)

@api.route('/getstudents',methods=['POST'])
@auth.login_required
def get_students_votein():
    data = request.get_json()
    vl_id = request.args.get('vl_id')
    votetype = request.args.get('votetype')
    if int(votetype) ==1:
        lists,totalnum = get_graduate(vl_id,data)
    else:
        lists,totalnum = get_excellent(vl_id,data)
    return SuccessPage(data=lists,totalnum=totalnum)

def get_graduate(vl_id,data):
    lists = db.session.query(Graduateresult.gr_id,Graduateresult.s_id,Graduateresult.vl_id,
                             Graduateresult.g_agreenum,Graduateresult.g_disagreenum,Graduateresult.g_abstained,
                             Graduateresult.d_agreenum,Graduateresult.d_disagreenum,Graduateresult.d_abstained,
                             Masterstudents.name,Masterstudents.account,Masterstudents.major,Masterstudents.title,
                             Masterstudents.tutor,Masterstudents.college,Masterstudents.thesisurl).filter(Graduateresult.vl_id == vl_id,Graduateresult.s_id == Masterstudents.s_id).limit(data['limit']).offset(data['offset']).all()
    totalres = db.session.query(func.count(Graduateresult.gr_id)).filter(Graduateresult.vl_id == vl_id, Graduateresult.s_id == Masterstudents.s_id).first()
    returnlist =[]
    for l in lists:
        templist = {}
        templist['gr_id'] = l[0]
        templist['s_id'] = l[1]
        templist['vl_id'] = l[2]
        templist['g_agreenum'] = l[3]
        templist['g_disagreenum'] = l[4]
        templist['g_abstained'] = l[5]
        templist['d_agreenum'] = l[6]
        templist['d_disagreenum'] = l[7]
        templist['d_abstained'] = l[8]
        templist['name'] = l[9]
        templist['account'] = l[10]
        templist['major'] = l[11]
        templist['title'] = l[12]
        templist['tutor'] = l[13]
        templist['college'] = l[14]
        templist['thesisurl'] = l[15]
        returnlist.append(templist)
    return returnlist,totalres[0]

def get_excellent(vl_id,data):
    list = db.session.query(Excellentresult.er_id,Excellentresult.s_id,Excellentresult.vl_id,
                            Excellentresult.agreenum,Excellentresult.disagreenum,Excellentresult.abstained,
                            Masterstudents.name,Masterstudents.account,Masterstudents.major,Masterstudents.title,
                             Masterstudents.tutor,Masterstudents.college,Masterstudents.thesisurl).filter(Excellentresult.vl_id == vl_id,Excellentresult.s_id == Masterstudents.s_id).limit(data['limit']).offset(data['offset']).all()
    totalres = db.session.query(func.count(Excellentresult.er_id)).filter(Excellentresult.vl_id == vl_id, Excellentresult.s_id == Masterstudents.s_id).first()

    returnlist = []
    for l in list:
        templist = {}
        templist['er_id'] = l[0]
        templist['s_id'] = l[1]
        templist['vl_id'] = l[2]
        templist['agreenum'] = l[3]
        templist['disagreenum'] = l[4]
        templist['abstained'] = l[5]
        templist['name'] = l[6]
        templist['account'] = l[7]
        templist['major'] = l[8]
        templist['title'] = l[9]
        templist['tutor'] = l[10]
        templist['college'] = l[11]
        templist['thesisurl'] = l[12]
        returnlist.append(templist)
    return returnlist,totalres[0]

@api.route('/get_havet_students')
@auth.login_required
def get_havenot_students():
    vl_id = request.args.get('vl_id')
    votetype = request.args.get('votetype')
    gr = Votelist.query.filter(Votelist.vl_id == vl_id).first()
    # print(gr['year'])
    grade = gr['year']
    if int(votetype) ==1:
        lists = get_havet_gradute(vl_id, grade)
    else:
        lists = get_havet_excellent(vl_id, grade)
    return Success(data=lists)

def get_havet_gradute(vl_id,grade):
    gradHaveNotList = db.session.query(Graduateresult.s_id).filter(Graduateresult.vl_id==vl_id).all()
    returnList = []
    for gl in gradHaveNotList:
        returnList.append(gl[0])
    # gradlist = Masterstudents.query.filter(Masterstudents.s_id.notin_(returnList)).all()
    gradlist = Masterstudents.query.filter(Masterstudents.grade == grade,Masterstudents.s_id.notin_(returnList)).all()
    return gradlist

def get_havet_excellent(vl_id,grade):
    exceHaveNotList = db.session.query(Excellentresult.s_id).filter(Excellentresult.vl_id==vl_id).all()
    returnList = []
    for gl in exceHaveNotList:
        returnList.append(gl[0])
    excelist = Masterstudents.query.filter(Masterstudents.grade == grade,Masterstudents.s_id.notin_(returnList)).all()
    return excelist


@api.route('/addvotertovoterin',methods=['POST'])
@auth.login_required
def add_voter_to_voterin():
    # 将投票人新增到voterin表中，代表该投票人参与了该次投票
    jsonData = request.get_json()
    # print(jsonData)
    # for voter in jsonData:
    #     # print(jsonData[voter])
    #     Voterin.add_voter_to_voterin(jsonData[voter]['vl_id'],jsonData[voter]['voter_id'])
    for voter in jsonData['data']:
        # print(jsonData[voter])
        Voterin.add_voter_to_voterin(voter['vl_id'],voter['voter_id'])
    return Success(msg='添加投票人成功',error_code=201)

@api.route('/addexcellentresult',methods=['POST'])
@auth.login_required
def add_excellentresult():
    jsonData = request.get_json()
    for excres in jsonData['data']:
        Excellentresult.add_result_to_excellent(
            excres['s_id'],
            excres['vl_id'],
            excres['agreenum'],
            excres['disagreenum'],
            excres['abstained'])
    return Success(msg='初始化优秀毕业生投票结果成功',error_code=201)

@api.route('/graduateresult',methods=['POST'])
@auth.login_required
def add_graduateresult():
    jsonData = request.get_json()
    for excres in jsonData['data']:
        Graduateresult.add_result_to_graduate(
            excres['s_id'],
            excres['vl_id'],
            excres['g_agreenum'],
            excres['g_disagreenum'],
            excres['g_abstained'],
            excres['d_agreenum'],
            excres['d_disagreenum'],
            excres['d_abstained'])
    return Success(msg='初始化毕业生毕业授予学位投票结果成功',error_code=201)

