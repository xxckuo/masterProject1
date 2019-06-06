import fractions

from flask import request, g
import flask_excel as excel
# from flask.ext import excel
from app.libs.error_code import Success, AuthFailed
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.excellentresult import Excellentresult
from app.models.graduateresult import Graduateresult
from app.models.masterstudents import Masterstudents
from app.models.votelist import Votelist
from app.models.voter import Voter

api = Redprint('voteresult')

@api.route('/get_vote_list')
def get_vote_list_by_votetype():
    votetype = request.args.get('votetype')
    voteres = Votelist.query.filter(Votelist.votetype == votetype).all()
    return Success(data=voteres)

@api.route('/exp_excel', methods=['GET'])
def exp_excel():
    vl_id = request.args.get('vl_id')
    votetype = request.args.get('votetype')
    filename = request.args.get('filename')
    print(filename)
    if int(votetype) == 1:
        # lists = get_graduate_excel(vl_id)
        q = db.session.query(Graduateresult.s_id.label('id'), Graduateresult.g_agreenum.label('毕业同意数'), Graduateresult.g_disagreenum.label('毕业不同意数'),
                               Graduateresult.g_abstained.label('毕业弃权数'),
                               Graduateresult.d_agreenum.label('授予硕士学位同意数'), Graduateresult.d_disagreenum.label('授予硕士学位不同意数'), Graduateresult.d_abstained.label('授予硕士学位弃权数'),
                               Masterstudents.name.label('姓名'), Masterstudents.account.label('学号'), Masterstudents.major.label('学科、领域'), Masterstudents.title.label('论文题目'),
                               Masterstudents.tutor.label('导师'),
                               Masterstudents.college.label('所在培养单位'), Masterstudents.thesisurl.label('链接')
                               ).filter(Graduateresult.s_id == Masterstudents.s_id,Graduateresult.vl_id ==vl_id)
        query_sets = q.all()
        return excel.make_response_from_query_sets(
            query_sets,
            column_names=[
                '姓名',
                # '专业',
                '学科、领域',
                '所在培养单位',
                # '学科、领域',
                '毕业同意数',
                '毕业不同意数',
                '毕业弃权数',
                '授予硕士学位同意数',
                '授予硕士学位不同意数',
                '授予硕士学位弃权数',
            ],
            file_type='xlsx',
            file_name= filename if filename !=None else '数据'+ '.xlsx'
        )
    else:
        # lists = get_excellent_excel(vl_id)
        q = db.session.query(Masterstudents.name.label('姓名'), Masterstudents.college.label('学科、领域'),
                             Masterstudents.title.label('论文题目'), Masterstudents.tutor.label('指导教师'),
                             Excellentresult.agreenum.label('同意数量'), Excellentresult.disagreenum.label('不同意数'),
                             Excellentresult.abstained.label('弃权')
                             ).filter(Excellentresult.vl_id == vl_id, Masterstudents.s_id == Excellentresult.s_id)
        query_sets = q.all()
        return excel.make_response_from_query_sets(
            query_sets,
            column_names=[
                '姓名',
                '学科、领域',
                '论文题目',
                '指导教师',
                '同意数量',
                '不同意数',
                '弃权'
            ],
            file_type='xlsx',
            file_name=filename if filename !=None else '数据'+ '.xlsx'
        )
