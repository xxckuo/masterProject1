from flask import current_app, jsonify, request,g
from app.libs.error_code import AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import Voter, auth
from app.models.base import db
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.votelist import Votelist
from app.models.voterin import Voterin

api = Redprint('votelist')

# 根据投票人uid获取他参与的所有投票
@api.route('/getlist', methods=['GET'])
@auth.login_required
def get_list():
    uid = g.voter.uid

    vls = db.session.query(Voterin.vl_id,Voterin.voterinstatus,Votelist.name,Votelist.year,Votelist.votetype,Votelist.votestatus,Votelist.votenum).filter(
        Voterin.voter_id==uid).filter(Voterin.vl_id==Votelist.vl_id).all()
    lists = []
    for vl in vls:
        list ={}
        list['vl_id'] = vl[0]
        list['voterinstatus'] = vl[1]
        list['name'] = vl[2]
        list['year'] = vl[3]
        list['votetype'] = vl[4]
        list['votestatus'] = vl[5]
        list['votenum'] = vl[6]
        lists.append(list)

    return Success(msg='查询列表成功',data = lists)






