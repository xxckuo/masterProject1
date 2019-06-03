from app.libs.redprint import Redprint


api = Redprint('masterstudents')

@api.route('/test')
def test():
    return 'hello world'