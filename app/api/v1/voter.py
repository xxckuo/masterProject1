from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.voter import Voter


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


