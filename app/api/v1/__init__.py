from flask import Blueprint
from app.api.v1 import voter, client, token, votelist, students, showresult, messages


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    voter.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    votelist.api.register(bp_v1)
    students.api.register(bp_v1)
    showresult.api.register(bp_v1)
    messages.api.register(bp_v1)

    return bp_v1
