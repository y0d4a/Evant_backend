from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Events
from blueprints.invitations.model import Invitations
from blueprints import db, app

import json

bp_events = Blueprint('events', __name__)
api = Api(bp_events)

class EventsResource(Resource):

    """
    class for event resources 
    """

    @jwt_required
    def post(self):

        """
        method to create new event
        """
        parser = reqparse.RequestParser()
        identity = get_jwt_identity()
       
        parser.add_argument('category', location='json', required=True)
        parser.add_argument('event_name', location='json', required=True)

        event_data = parser.parse_args()

        creator_id = int(identity['user_id'])
        category = event_data['category']
        event_name = event_data['event_name']
        status = 0

        event = Events(creator_id, category, event_name, status)
        print(type(event))

        db.session.add(event)
        db.session.commit()

        return marshal(event, Events.response_fields), 200, {'Content-Type':'application/json'}

    @jwt_required
    def put(self, event_id):

        """
        method to edit events
        """
        parser = reqparse.RequestParser()
        identity = get_jwt_identity()
        creator_id = int(identity['user_id'])

        parser.add_argument('category', location='json', required=False)
        parser.add_argument('event_name', location='json', required=False)
        parser.add_argument('status', location='json', required=False)
        parser.add_argument('place_name', location='json', required=False)
        parser.add_argument('place_location', location='json', required=False)
        parser.add_argument('start_date', location='json', required=False)
        parser.add_argument('end_date', location='json', required=False)
        parser.add_argument('start_date_parameter', location='json', required=False)
        parser.add_argument('end_date_parameter', location='json', required=False)
        parser.add_argument('duration', location='json', required=False)

        event_data = parser.parse_args()

        event_query = Events.query.get(event_id)

        if event_query is None:
            return {'status':'event not found'}, 404
        
        if event_data['category'] is not None:
            event_query.category = event_data['category'] 
        if event_data['event_name'] is not None:
            event_query.event_name = event_data['event_name'] 
        if event_data['status'] is not None:
            event_query.status = event_data['status'] 
        if event_data['place_name'] is not None:
            event_query.place_name = event_data['place_name']
        if event_data['place_location'] is not None:
            event_query.place_location = event_data['place_location'] 
        if event_data['start_date'] is not None:
            event_query.start_date = event_data['start_date'] 
        if event_data['end_date'] is not None:
            event_query.end_date = event_data['end_date'] 
        if event_data['start_date_parameter'] is not None:
            event_query.start_date_parameter = event_data['start_date_parameter'] 
        if event_data['end_date_parameter'] is not None:
            event_query.end_date_parameter = event_data['end_date_parameter'] 
        if event_data['duration'] is not None:
            event_query.duration = event_data['duration']  
        
        db.session.commit()

        return marshal(event_query, Events.response_fields), 200, {'Content-Type' : 'application/json'}
    
    @jwt_required
    def get(self, event_id):

        """
        method to get event detail by id
        """
        event_query = Events.query.get(event_id)

        if event_query is None:
            return {'status':'event not found'}, 404
        
        return marshal(event_query, Events.response_fields), 200, {'Content-Type' : 'application/json'}


class EventsOngoingResource(Resource):

    """
    method to edit events
    """
    
    @jwt_required
    def get(self):

        """
        method to get all ongoing events
        """
        identity = get_jwt_identity()
        user_id = identity['user_id']

        invitation_query = Invitations.query.filter_by(invited_id=user_id, status=1).all()

        list_event = []

        for invitaion in invitation_query:
            event_id = invitaion.event_id
            event_query = Events.query.get(event_id)
            if event_query.status == 0:
                list_event.append(marshal(event_query, Events.response_fields))
        
        return list_event, 200, {'Content-Type' : 'application/json'}


class EventsHistoryResource(Resource):

    """
    method to edit events
    """
    
    @jwt_required
    def get(self):

        """
        method to get all ongoing events
        """
        identity = get_jwt_identity()
        user_id = identity['user_id']

        invitation_query = Invitations.query.filter_by(invited_id=user_id, status=1).all()

        list_event = []

        for invitaion in invitation_query:
            event_id = invitaion.event_id
            event_query = Events.query.get(event_id)
            if event_query.status == 1:
                list_event.append(marshal(event_query, Events.response_fields))
        
        return list_event, 200, {'Content-Type' : 'application/json'}

api.add_resource(EventsResource, '','/<event_id>')
api.add_resource(EventsOngoingResource, '/ongoing')
api.add_resource(EventsHistoryResource, '/history')
