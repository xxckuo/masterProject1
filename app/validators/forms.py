from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.voter import Voter
from app.validators.base import BaseForm as Form

class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    # type = IntegerField(validators=[DataRequired()])

    # def validate_type(self, value):
    #     try:
    #         client = ClientTypeEnum(value.data)
    #     except ValueError as e:
    #         raise e
    #     self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[DataRequired(message='不允许为空')])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if Voter.query.filter_by(teacher_account=value.data).first():
            raise ValidationError(message='已有该账户，勿重复注册')


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
