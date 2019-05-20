from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.votelist import Votelist
from app.models.voter import Voter
from app.models.voterin import Voterin

api = Redprint('user')

@api.route('/listget', methods=['GET'])
@auth.login_required
def get_list():
    uid = g.voter.uid
    datas = {}
    vls = db.session.query(Voterin.vl_id,Votelist.name,Votelist.year,Votelist.votetype,Votelist.votestatus,Votelist.votenum).filter(
        Voterin.voter_id==uid,Voterin.voterinstatus==0).filter(Voterin.vl_id==Votelist.vl_id).all()
    lists = []
    for vl in vls:
        list ={}
        list['votelist_name'] = vl[1]
        list['votelist_year'] = vl[2]
        list['votelist_votetype'] = vl[3]
        list['votelist_votestatus'] = vl[4]
        list['votelist_votenum'] = vl[5]
        lists.append(list)
    print(lists)

    return Success(msg='查询列表成功')


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


