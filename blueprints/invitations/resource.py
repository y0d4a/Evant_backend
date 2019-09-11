from flask import Blueprint
from flask_restful import Api
from .model import Invitations

bp_invitations = Blueprint('invitations', __name__)
api = Api(bp_invitations)

