from flask import request, jsonify

from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.voter import Voter
from app.validators.forms import ClientForm, UserEmailForm
from app.libs.enums import ClientTypeEnum
from werkzeug.exceptions import HTTPException


api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[ClientTypeEnum(100)]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    Voter.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)
