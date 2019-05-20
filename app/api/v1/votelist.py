from flask import current_app, jsonify, request
from app.libs.error_code import AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import Voter
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.votelist import Votelist
from app.models.voterin import Voterin

api = Redprint('votelist')

@api.route('/createlist',methods=['POST'])
def create_list():
    jsonData = request.get_json()
    Votelist.add_votelist(jsonData['name'],jsonData['year'],jsonData['votetype'],jsonData['votestatus'],jsonData['votenum'])
    return Success(msg='新增成功',error_code=201)

@api.route('/addvotertovoterin',methods=['POST'])
def add_voter_to_voterin():
    # 将投票人新增到voterin表中，代表该投票人参与了该次投票
    jsonData = request.get_json()
    for voter in jsonData['data']:
        Voterin.add_voter_to_voterin(voter['vl_id'],voter['voter_id'])
    return Success(msg='添加投票人成功')

@api.route('/addexcellentresult',methods=['POST'])
def add_excellentresult():
    jsonData = request.get_json()
    for excres in jsonData['data']:
        Excellentresult.add_result_to_excellent(
            excres['s_id'],
            excres['vl_id'],
            excres['agreenum'],
            excres['disagreenum'],
            excres['abstained'])
    return Success(msg='初始化优秀毕业生投票结果成功')

@api.route('/graduateresult',methods=['POST'])
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
    return Success(msg='初始化毕业生毕业授予学位投票结果成功')