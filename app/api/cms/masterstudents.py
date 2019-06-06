import os
import time
import xlrd
import urllib.request
from flask import request
from app.models.base import db
from app.models.masterstudents import Masterstudents
from app.libs.error_code import  Success
from app.libs.redprint import Redprint
import urllib
import urllib.error
import requests


api = Redprint('masterstudents')


@api.route('/excel_add',methods = ['POST'])
def master():
    jsonData = request.get_json()
    BASE_DIR = os.path.dirname(__file__)
    print(BASE_DIR)
    url = "https://mastera.oss-cn-beijing.aliyuncs.com/student.xlsx?Expires=1559822601&OSSAccessKeyId=TMP.AgE-JRsLpo-9vtgtIE9jvUF9zu2GNu1cpI_nNENWRLPtMpQP6EEx_Dqc-Rz-ADAtAhR4YVgl8J6iJGix9ZAuWoT6aFGnfAIVALC40lDdIMZ1s3ELL8xf7-ECU-EA&Signature=zQF9EX1G6uravV4eVzx6yhhlveM%3D"
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
            masterstudents.tutor = a[4]
            masterstudents.college = a[5]
            masterstudents._password = a[0]
            db.session.add(masterstudents)
    os.remove(downPath)
    end = time.time()
    print(end - start)
    return Success(msg='新增学生信息成功')

@api.route('/select_students')
def select_student():
        data = request.args.get("s_id")
        student_message = Masterstudents.query.filter(Masterstudents.s_id ==data).all()
        student_messages = []
        for me in student_message:
            student_messages.append(me.to_json())
        return Success(msg='查找成功', data=student_messages)

@api.route('/alter',methods= ['POST'])
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
            masterstudents.account = data["account"]
            masterstudents.title = data["title"]
            return Success(msg='修改成功')

@api.route('/input_student',methods= ['POST'])
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
        masterstudents._password = data["password"]
        masterstudents.thesisurl = data["thesisurl"]
        db.session.add(masterstudents)
        return Success(msg='增加成功')


@api.route('/delete')
def delete_student():
   s_id = request.args.get('s_id')
   with db.auto_commit():
       messages = Masterstudents.query.filter(Masterstudents.s_id==s_id).first()
       messages.status = 0

   return Success(msg='删除学生信息成功')
@api.route('/select_students')
def select():
    masterstudent = Masterstudents.query(Masterstudents.account).all()
    # a = db.session.query
    # masterstudents= []
    # for stu in masterstudent:
    #     masterstudents.append(stu.to_json())
    return Success(msg='查找成功',data=masterstudent)


