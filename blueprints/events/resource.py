from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Events
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

        return marshal(event, Events.response_field), 200, {'Content-Type':'application/json'}

api.add_resource(EventsResource, '')


        