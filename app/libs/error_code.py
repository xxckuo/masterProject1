from werkzeug.exceptions import HTTPException

from app.libs.error import APIException, APIExceptions


class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0
    data = dict()

class SuccessPage(APIExceptions):
    code = 200
    msg = 'ok'
    error_code = 0
    data = dict()
    totalnum = 0

class DeleteSuccess(Success):
    code = 202
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999


class ClientTypeError(APIException):
    # 400 401 403 404
    # 500
    # 200 201 204
    # 301 302
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001

class SqlError(APIException):
    code = 200
    msg = '数据已存在数据库'
    error_code = 1001

class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = '账号密码出错，请重新输入'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'
