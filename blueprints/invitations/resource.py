from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Invitations
from blueprints.events.model import Events
from blueprints.users.model import Users
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
        
        list_event_temporrary = []

        for event in invitations_query:
            event_new = marshal(event, Invitations.response_fields)
            event_id = event_new['event_id']
            from_event_table = Events.query.get(event_id)
            from_event_table = marshal(from_event_table, Events.response_fields)
            
            creator = Users.query.get(from_event_table['creator_id'])
            creator = marshal(creator, Users.response_fields)

            response_fields_dummy = {
                'event_id' : from_event_table['event_id'],
                'event_name' : from_event_table['event_name'],
                'invited_id' : event_new['invited_id'],
                'creator_id' : creator['user_id'],
                'username_creator' : creator['username'],
                'status' : event_new['status']
            }
            list_event_temporrary.append(response_fields_dummy)
    
        return list_event_temporrary, 200, {'Content-Type':'application/json'}
    
    @jwt_required
    def post(self):

        """
        method to invite someone to an event
        """
        parser = reqparse.RequestParser()
        identity = get_jwt_identity()
        user_id = int(identity['user_id'])

        # parser.add_argument('event_id', location='json', required=True)
        parser.add_argument('invited_id', location='json', required=True)
        invitation_data = parser.parse_args()

        ''' Take all event id by creator_id '''
        events = Events.query.filter_by(creator_id = user_id)

        ''' Take newest event_id '''
        event = events[-1]
        event = marshal(event, Events.response_fields)

        event_id = event['event_id']
        invited_id = invitation_data['invited_id']

        ''' Add to init model '''
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
