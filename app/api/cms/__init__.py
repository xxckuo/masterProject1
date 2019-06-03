from flask import Blueprint
from app.api.cms import masterstudents, voter, votelist, voteresult


def create_blueprint_cms():
    bp_cms = Blueprint('cms', __name__)
    masterstudents.api.register(bp_cms)
    voter.api.register(bp_cms)
    votelist.api.register(bp_cms)
    voteresult.api.register(bp_cms)
    return bp_cms
