import time

from flask import jsonify, g, request

from app.libs.error_code import DeleteSuccess, AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.votelist import Votelist
from app.models.voter import Voter
from app.models.voterin import Voterin

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = Voter.query.filter_by(id=uid).first_or_404(msg='暂无该用户信息')
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.voter.uid
    user = Voter.query.filter_by(id=uid).first_or_404(msg='mei zhao dao')
    return jsonify(user)


# 管理员
@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    pass


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.voter.uid
    with db.auto_commit():
        user = Voter.query.filter_by(id=uid).first_or_404(msg='mei zhao dao')
        user.delete()
    return DeleteSuccess()


@api.route('', methods=['PUT'])
def update_user():
    return 'update qiyue'

@api.route('/uploadvoteresult',methods=['POST'])
@auth.login_required
def upload_vote_result():
    # 投票结果的上传
    jsonData = request.get_json()
    Voterin.update_voter_status(jsonData['vl_id'], jsonData['voter_id'])
    if int(jsonData['votetype']) ==1:
        upload_graduate(jsonData)
    else:
        upload_excellent(jsonData)
    res = Voterin.check_vote_and_update_status(jsonData['vl_id'])
    if res:
        # 将投票列表的状态置为已经完成投票
        Votelist.update_votelist_status(jsonData['vl_id'])
    return Success(msg='投票成功')


def upload_excellent(jsonData):
    # 上传到优秀毕业生投票结果表
    for res in jsonData['data']:
        # if int(res['excellent_result']) != 0:
        Excellentresult.update_excellent_result_by_all(res['gr_id'],res['excellent_result'])

def upload_graduate(jsonData):
    # 上传到学生毕业和是否授予学位的表
    # start = time.time()
    for res in jsonData['data']:
        if int(res['graduate_result']) != 0 or int(res['degree_result']) != 0:
            Graduateresult.update_graduatew_result_by_all(res['gr_id'],res['graduate_result'],res['degree_result'])

    # Graduateresult.update_graduatew_result_by_all(jsonData['data'])

    # end = time.time()
    # print(end - start)