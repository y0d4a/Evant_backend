from flask import Blueprint
# from datetime import timedelta, date
import json
import datetime
import operator
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Events
from blueprints.invitations.model import Invitations
from blueprints.available_dates.model import AvailableDates
from blueprints.user_preferences.model import UserPreferences
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
        parser.add_argument('preference', location='json', required=False)
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
        if event_data['preference'] is not None:
            event_query.preference = event_data['preference'] 
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

class EventsPreferenceResource(Resource):

    """
    class to edit/add preference which is the the dominant preference from all member
    """
    
    @jwt_required
    def get(self, event_id):
        """
        function to get dominant preferences
        """
        creator = get_jwt_identity()
        preferences = UserPreferences.query.filter_by(event_id = event_id)
        
        '''
        get all user preference
        '''
        list_for_save_preferences = []
        for value in preferences:
            new_value = marshal(value, UserPreferences.response_fields)
            list_for_save_preferences.append(new_value['preference'])

        '''
        find the difference preference in preferences
        '''
        list_different_preferences = []
        for value in list_for_save_preferences:
            if value not in list_different_preferences:
                list_different_preferences.append(value)
        
        dictionary_count_value = {}
        for value in list_different_preferences:
            dictionary_count_value[value] = list_for_save_preferences.count(value)
        
        dominant_preference = max(dictionary_count_value.items(), key=operator.itemgetter(1))[0]

        return {"dominant_preference" : dominant_preference, "dictionary_count_value": dictionary_count_value}, 200, {'Content-Type' : 'application/json'}

class EventsDatesGenerateResource(Resource):

    """
    class to generate date    """

    def get(self, event_id):
        '''
        get creator_id by event id
        '''
        creator_query = Events.query.get(event_id)
        creator = marshal(creator_query, Events.response_fields)
        creator_id = creator['creator_id']

        # list_of_id = [creator_id]
        list_of_id = []
        invitation_query = Invitations.query.filter_by(event_id = event_id)
        for invitation in invitation_query:
            invitation_new = marshal(invitation, Invitations.response_fields)
            list_of_id.append(invitation_new['invited_id'])

        dictionary_date = {}
        for user_id in list_of_id:
            date = AvailableDates.query.filter_by(user_id = user_id)
            list_temporary_date = []
            for value in date:
                value_new = marshal(value, AvailableDates.response_fields)
                list_temporary_date.append(int(value_new['date'][0:2]))
            dictionary_date[user_id] = list_temporary_date

        event_query = Events.query.get(event_id)
        event = marshal(event_query, Events.response_fields)
        duration = event['duration']

        start_date_parameter = event['start_date_parameter']
        new_dt_start = start_date_parameter[:19]
        end_date_parameter = event['end_date_parameter']
        new_dt_end = end_date_parameter[:19]
                
        # start_day = int(start_date_parameter[0:2])
        # start_month = int(start_date_parameter[3:5])
        # start_year = int(start_date_parameter[6:10])

        # end_day = int(end_date_parameter[0:2])
        # end_month = int(end_date_parameter[3:5])
        # end_year = int(end_date_parameter[6:10])
        
        # start_dt = date(start_year, start_month, start_day)
        # end_dt = date(end_year, end_month, end_day)
        
        # diff= (end_dt-start_dt).days+1
        
        start = datetime.datetime.strptime(new_dt_start, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(new_dt_start, '%Y-%m-%d %H:%M:%S')
        step = datetime.timedelta(days=1)

        # def daterange(date1, date2):
        #     for n in range(int ((date2 - date1).days)+1):
        #     yield date1 + timedelta(n)
        
        date_interval = {}
        # for dt in range(diff):
        #     date_interval.append(start_dt+datetime.timedelta(dt))
        
        while start <= end:
            date_interval(start.date())
            start += step

        return json.dumps(date_interval),200


        return start_date_parameter, 200


        return dictionary_date, 200


api.add_resource(EventsResource, '','/<event_id>')
api.add_resource(EventsOngoingResource, '/ongoing')
api.add_resource(EventsHistoryResource, '/history')
api.add_resource(EventsPreferenceResource, '/dominant_preference/<event_id>')
api.add_resource(EventsDatesGenerateResource, '/generate_date/<event_id>')


