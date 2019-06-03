
import xlrd
import requests
from flask import request

from app.models.base import db
from app.models.masterstudents import Masterstudents
from app.libs.error_code import  Success
from app.libs.redprint import Redprint

api = Redprint('masterstudents')


@api.route('/excel_add')
def master():
    path = 'D:/student.xlsx'
    workbook = xlrd.open_workbook(path)

    Data_sheet = workbook.sheets()[0]  # 通过索引获取

    rowNum = Data_sheet.nrows  # sheet行数
    colNum = Data_sheet.ncols  # sheet列数
    #

    list = []
    for i in range(rowNum):
        rowlist = []
        for j in range(colNum):
            rowlist.append(Data_sheet.cell_value(i, j))
        list.append(rowlist)
    del list[0]
    # print(list)
    for a in list:
        with db.auto_commit():
            masterstudents = Masterstudents()
            masterstudents.account= a[0]
            masterstudents.name = a[1]
            masterstudents.major = a[2]
            masterstudents.title = a[3]
            masterstudents.tutor = a[4]
            masterstudents.college = a[5]
            masterstudents._password = a[0]
            db.session.add(masterstudents)

    return Success(msg='新增学生信息成功')

@api.route('/select_students')
def select():
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

