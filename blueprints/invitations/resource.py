from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Invitations
from blueprints import db, app

import json

bp_invitations = Blueprint('invitations', __name__)
api = Api(bp_invitations)

class InvitationsResource(Resource):

    """
    class for invitations resource
    """

    @jwt_required
    def get(self):

        """
        method to get all invitations 
        """
        identity = get_jwt_identity()
        user_id = int(identity['user_id'])

        invitations_query = Invitations.query.filter_by(invited_id=user_id, status=0).all()

        if invitations_query is None:
            return {'status':'no invitations'}, 200

        invitations_json = marshal(invitations_query, Invitations.response_fields)

        return invitations_json, 200, {'Content-Type':'application/json'}
    
    @jwt_required
    def post(self):

        """
        method to invite someone to an event
        """
        parser = reqparse.RequestParser()
        identity = get_jwt_identity()
        user_id = int(identity['user_id'])

        parser.add_argument('event_id', location='json', required=True)
        parser.add_argument('invited_id', location='json', required=True)

        invitation_data = parser.parse_args()
        
        event_id = invitation_data['event_id']
        invited_id = invitation_data['invited_id']

        invitation = Invitations(event_id, invited_id, 0)

        db.session.add(invitation)
        db.session.commit()

        return marshal(invitation, Invitations.response_fields), 200, {'Content-Type':'application/json'}
    
    @jwt_required
    def put(self, event_id):

        """
        method to accept invitation
        """
        identity = get_jwt_identity()
        user_id = int(identity['user_id'])

        invitations_query = Invitations.query.filter_by(event_id=event_id, invited_id=user_id, status=0).first()

        if invitations_query is None:
            return {'status':'no invitations'}, 404
        
        invitations_query.status = 1
        db.session.commit()

        return marshal(invitations_query, Invitations.response_fields), 200, {'Content-Type':'application/json'}

class InvitationsRejectResource(Resource):

    """
    class for reject invitations
    """
    @jwt_required
    def put(self, event_id):

        """
        method to reject invitation
        """
        identity = get_jwt_identity()
        user_id = int(identity['user_id'])

        invitations_query = Invitations.query.filter_by(event_id=event_id, invited_id=user_id, status=0).first()

        if invitations_query is None:
            return {'status':'no invitations'}, 404
        
        invitations_query.status = -1
        db.session.commit()

        return marshal(invitations_query, Invitations.response_fields), 200, {'Content-Type':'application/json'}

api.add_resource(InvitationsResource, '', '/accept/<event_id>')
api.add_resource(InvitationsRejectResource, '', '/reject/<event_id>')
