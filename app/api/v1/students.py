from flask import current_app, jsonify, request
from app.libs.error_code import AuthFailed, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import Voter
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.masterstudents import Masterstudents
from app.models.votelist import Votelist
from app.models.voterin import Voterin

api = Redprint('students')

@api.route('/addstudents',methods=['POST'])
def add_students():
    jsonData = request.get_json()
    Masterstudents.add_student(jsonData['name'],jsonData['account'],jsonData['major'],jsonData['title'],jsonData['tutor'],jsonData['college'],jsonData['thesisurl'])
    return Success(msg='新增学生成功', error_code=201)