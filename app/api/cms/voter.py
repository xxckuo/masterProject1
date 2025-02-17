import os
import urllib.request
import requests
import time

from flask import request
from sqlalchemy import func

from app.libs.error_code import AuthFailed, Success, SqlError, SuccessPage
from app.libs.redprint import Redprint
import xlrd

from app.libs.token_auth import auth
from app.models.voter import Voter
from app.models.base import db
from app.api.cms.base import File


api = Redprint('voter')
# 小菜鸟

@api.route('/show',methods = ['POST'])
# @auth.login_required
def voter_show():

    data = request.get_json()

    list = Voter.query.filter(Voter.status==1).limit(data['limit']).offset(data['offset']).all()

    # total = db.session.query(func.count(Voter.id)).first()
    total = db.session.query(func.count(Voter.id)).filter(Voter.status==1).first()
    totalnum = total[0]

    data = []

    for voter in list:
        voters = {}
        voters['voter_id']=voter.id
        voters['voter_account']=voter.teacher_account
        voters['voter_name']=voter.nickname

        voters['auth'] = voter.auth
        data.append(voters)

    return SuccessPage(msg='查询成功', data=data,totalnum=totalnum)




@api.route('/addlist',methods = ['POST'])
@auth.login_required
def voter_post():

    data = request.get_json()
    File.download(data['url'],data['filename'])

    curPath = os.getcwd()
    url = xlrd.open_workbook(curPath+'\\excel文档'+'\\'+data['filename'])
    table = url.sheets()[0]
    nrows = table.nrows  # 行数
    row_list = [table.row_values(i) for i in range(1, nrows)]  # 所有行的数据
    add_voterlist(row_list)

    # 删除文件
    File.delete(data['filename'])
    return Success(msg = '批量导入教师成功')


@api.route('/add',methods=['POST'])
@auth.login_required
def voter():
    jsonData = request.get_json()
    if Voter.query.filter(Voter.teacher_account==jsonData['teacher_account']).first():
        raise AuthFailed(msg ='该老师已存在')
    else:
        add_voter(jsonData['teacher_account'],jsonData['nickname'])
    return Success(msg='老师新增成功')

@api.route('/update',methods=['POST'])
@auth.login_required
def update():
    data = request.get_json()
    # 传一个条件代表删除
    msg = Voter.update_voter(data)
    return Success(msg=msg)


def add_voter(teacher_account,nickname):
    with db.auto_commit():
        voter = Voter()
        voter.nickname = nickname
        voter.teacher_account = teacher_account
        voter.password = teacher_account
        voter.auth =1
        db.session.add(voter)


def add_voterlist(rowlist):
    # start = time.time()
    with db.my_auto_commit():
        for list in rowlist:
            voter = Voter()
            voter.nickname = list[1]
            voter.teacher_account = list[0]
            voter.password = list[0]
            voter.auth =1
            db.session.add(voter)

    # print('交话费')
    # end = time.time()
    # print(end - start)