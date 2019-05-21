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

    vls = db.session.query(Voterin.vl_id,Voterin.voterinstatus,Votelist.name,Votelist.year,Votelist.votetype,Votelist.votestatus,Votelist.votenum).filter(
        Voterin.voter_id==uid).filter(Voterin.vl_id==Votelist.vl_id).all()
    lists = []
    for vl in vls:
        list ={}
        list['voterin_vl+id'] = vl[0]
        list['voterin.voterinstatus'] = vl[1]
        list['votelist_name'] = vl[2]
        list['votelist_year'] = vl[3]
        list['votelist_votetype'] = vl[4]
        list['votelist_votestatus'] = vl[5]
        list['votelist_votenum'] = vl[6]
        lists.append(list)


    return Success(msg='查询列表成功',data = lists)


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


