from .app import Flask


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    from app.api.cms import create_blueprint_cms
    app.register_blueprint(create_blueprint_v1(), url_prefix='/master/v1')
    app.register_blueprint(create_blueprint_cms(), url_prefix='/master/cms')


def register_plugin(app):
    from app.models.base import db
    from app.models.excellentresult import Excellentresult
    from app.models.graduateresult import Graduateresult
    from app.models.masterstudents import Masterstudents
    from app.models.votelist import Votelist
    from app.models.voterin import Voterin

    db.init_app(app)
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprints(app)
    register_plugin(app)

    return app

