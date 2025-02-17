import os
import time
import xlrd
import urllib.request
from flask import request
from sqlalchemy import func

from app.libs.token_auth import auth
from app.models.base import db
from app.models.masterstudents import Masterstudents
from app.libs.error_code import Success, SuccessPage
from app.libs.redprint import Redprint
import urllib
import urllib.error
import requests


api = Redprint('masterstudents')


@api.route('/get_grade')
@auth.login_required
def get_grade():
    grade = db.session.query(Masterstudents.grade).group_by(Masterstudents.grade).order_by(Masterstudents.grade.desc()).all()
    returndata = []
    for g in grade:
        returndata.append(g[0])

    return Success(data=returndata)

@api.route('/excel_add',methods = ['POST'])
@auth.login_required
def master():

    jsonData = request.get_json()
    BASE_DIR = os.path.dirname(__file__)
    print(BASE_DIR)
    url = jsonData['url']
    downPath = BASE_DIR+'\\'+jsonData["filename"]
    a = urllib.request.urlretrieve(url, downPath)

    path = downPath
    workbook = xlrd.open_workbook(path)

    Data_sheet = workbook.sheets()[0]  # 通过索引获取
    rowNum = Data_sheet.nrows  # sheet行数
    colNum = Data_sheet.ncols  # sheet列数

    list = []
    for i in range(rowNum):
        rowlist = []
        for j in range(colNum):
            rowlist.append(Data_sheet.cell_value(i, j))
        list.append(rowlist)
    del list[0]
    # print(list)

    start = time.time()

    with db.auto_commit():
        for a in list:
            masterstudents = Masterstudents()
            masterstudents.account= a[0]
            masterstudents.name = a[1]
            masterstudents.major = a[2]
            masterstudents.title = a[3]
            masterstudents.thesisurl = a[7]
            masterstudents.tutor = a[4]
            masterstudents.college = a[5]
            masterstudents.grade = a[6]
            masterstudents._password = a[0]
            db.session.add(masterstudents)
    os.remove(downPath)
    end = time.time()
    print(end - start)
    return Success(msg='新增学生信息成功')

#根据学生id查找学生
@api.route('/select_students')
@auth.login_required
def select_students():
        s_id = request.args.get('s_id')
        student_message = Masterstudents.query.filter(Masterstudents.s_id == s_id).all()
        return Success(msg='查找成功', data=student_message)

@api.route('/alter',methods= ['POST'])
@auth.login_required
def alter():
        data = request.get_json()
        with db.auto_commit():
            masterstudents = Masterstudents.query.filter(Masterstudents.s_id == data["s_id"]).first()
            masterstudents.name= data["name"]
            masterstudents.tutor = data["tutor"]
            masterstudents.password = data["password"]
            masterstudents.thesisurl = data["thesisurl"]
            masterstudents.college = data["college"]
            masterstudents.major= data["major"]
            masterstudents.grade= data["grade"]
            masterstudents.account = data["account"]
            masterstudents.title = data["title"]
            return Success(msg='修改成功')

@api.route('/input_student',methods= ['POST'])
@auth.login_required
def input_student():
    data = request.get_json()
    with db.auto_commit():
        masterstudents = Masterstudents()
        masterstudents.name = data["name"]
        masterstudents.account = data["account"]
        masterstudents.major = data["major"]
        masterstudents.title = data["title"]
        masterstudents.tutor = data["tutor"]
        masterstudents.college = data["college"]
        masterstudents.grade = data["grade"]
        masterstudents._password = data["password"]
        masterstudents.thesisurl = data["thesisurl"]
        db.session.add(masterstudents)
        return Success(msg='增加成功')


@api.route('/delete')
@auth.login_required
def delete_student():
   s_id = request.args.get('s_id')
   with db.auto_commit():
       # 删除学生接口未验证学生是否存在
       messages = Masterstudents.query.filter(Masterstudents.s_id==s_id).first()
       messages.status = 0
   return Success(msg='删除学生信息成功')

#根据学生年级查找
@api.route('/select',methods = ['POST'])
@auth.login_required
def select():
    data = request.get_json()
    if data['grade']== '':
        masterstudent = Masterstudents.query.filter(Masterstudents!=0).limit(data['limit']).offset(data['offset']).all()
        total = db.session.query(func.count(Masterstudents.s_id)).filter(Masterstudents!=0).first()
        totalnum = total[0]
    else:
        masterstudent =Masterstudents.query.filter(Masterstudents.grade == data['grade'],Masterstudents.status!=0).limit(data['limit']).offset(data['offset']).all()
        total = db.session.query(func.count(Masterstudents.s_id)).filter(Masterstudents.grade == data['grade'],Masterstudents.status!=0).first()
        totalnum = total[0]
    return SuccessPage(msg='查找成功', data=masterstudent,totalnum=totalnum)


