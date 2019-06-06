import requests

from flask import request

from app.libs.error_code import AuthFailed, Success, SqlError
from app.libs.redprint import Redprint
import xlrd

from app.models.voter import Voter
from app.models.base import db

api = Redprint('voter')
# 小菜鸟

@api.route('/addlist',methods = ['POST'])
def voter_post():
    data = request.get_json()
    Download_url = data['url']
    r = requests.get(Download_url)
    f = open("教师3.xls","wb")
    f.write(r.content)
    f.close()

    url = xlrd.open_workbook(r'D:\Pythonprogram\masterProject1\教师3.xls')
    table = url.sheets()[0]
    nrows = table.nrows  # 行数
    row_list = [table.row_values(i) for i in range(1, nrows)]  # 所有行的数据
    add_voterlist(row_list)
    return Success(msg = '批量导入教师成功')


@api.route('/add',methods=['POST'])
def voter():
    jsonData = request.get_json()
    if Voter.query.filter(Voter.teacher_account==jsonData['teacher_account']).first():
        raise AuthFailed(msg ='该老师已存在')
    else:
        add_voter(jsonData['teacher_account'],jsonData['nickname'])
    return Success(msg='老师新增成功')

@api.route('/update',methods=['POST'])
def update():
    data = request.get_json()
    # 传一个条件代表删除
    Voter.update_voter(data)
    return Success(msg='修改老师信息成功')


def add_voter(teacher_account,nickname):
    with db.auto_commit():
        voter = Voter()
        voter.nickname = nickname
        voter.teacher_account = teacher_account
        voter.password = teacher_account
        voter.auth =1
        db.session.add(voter)

def add_voterlist(rowlist):
    with db.my_auto_commit():
        for list in rowlist:
            voter = Voter()
            voter.nickname = list[1]
            voter.teacher_account = list[0]
            voter.password = list[0]
            voter.auth =1
            db.session.add(voter)
