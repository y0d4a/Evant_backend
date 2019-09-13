from flask import Blueprint
import json
import datetime
import operator
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import Events
from blueprints.invitations.model import Invitations
from blueprints.available_dates.model import AvailableDates
from blueprints.user_preferences.model import UserPreferences
from blueprints.users.model import Users
from blueprints import db, app

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

    @jwt_required
    def delete(self, event_id):

        """
        method to delete event based on event_id
        """
        event_query = Events.query.get(event_id)

        if event_query is None:
            return {'status':'event not found'}, 404
        
        db.session.delete(event_query)
        db.session.commit()

        return {'status':'delete success'}, 200

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
        find the difference preference in preferences
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

    @jwt_required
    def get(self, event_id):
        '''
        get creator_id by event id
        '''
        creator_query = Events.query.get(event_id)
        creator = marshal(creator_query, Events.response_fields)
        creator_id = creator['creator_id']

        list_of_id = []
        
        '''
        get all invited_id
        '''
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
                list_temporary_date.append(value_new['date'])
            dictionary_date[user_id] = list_temporary_date


        '''
        get event duration
        '''
        event_query = Events.query.get(event_id)
        event = marshal(event_query, Events.response_fields)
        duration = event['duration']


        '''
        get event start/end_date_parameter
        '''
        start_date_parameter = event['start_date_parameter']
        new_dt_start = start_date_parameter[:10]
        end_date_parameter = event['end_date_parameter']
        new_dt_end = end_date_parameter[:10]

        '''
        generate date interval
        '''
        date_interval = []
        start = datetime.datetime.strptime(new_dt_start, "%Y-%m-%d")
        end = datetime.datetime.strptime(new_dt_end, "%Y-%m-%d")
        date_generated = [start + datetime.timedelta(days=dt) for dt in range(0, ((end-start).days)+1)]

        for date in date_generated:
            date_interval.append(date.strftime("%d/%m/%Y"))
        
        '''
        slicing the interval date into sub interval
        ''' 
        slicing_date = {}
        for index in range(0, (len(date_interval)-duration)+1):
            list_date_match_tem = []
            list_date_interval = date_interval[index:(duration+index)]
            slicing_date[str(index)] = list_date_interval
        
        '''
        match the date of every passenger in interval range
        '''
        date_match = {}
        list_date_match = []
        list_date_most_match = []
        list_attendace_match = []
        list_attendance_most_match = []
        
        for index, value in slicing_date.items():
            dict_user_opinion = {}
            agreement_count = 0
           
            for user_id in dictionary_date:
                if(set(value).issubset(set(dictionary_date[user_id]))):
                    user_query = Users.query.get(user_id)
                    user = marshal(user_query, Users.response_fields)
                    username = user['username']
                    dict_user_opinion[username] = "Bisa"
                    agreement_count += 1
                else:
                    user_query = Users.query.get(user_id)
                    user = marshal(user_query, Users.response_fields)
                    username = user['username']
                    dict_user_opinion[username] = "Tidak Bisa"

            if len(dictionary_date) == agreement_count:
                date_match["result"+index] = "ALL OF YOU CAN ATTEND IN THIS DATES"   
                list_date_match.append(value)
                list_attendace_match.append(dict_user_opinion)
            elif (len(dictionary_date)/2) > agreement_count:
                date_match["result"+index] = "DATES NOT FOUND"        
            else :
                date_match["result"+index] = "MOST OF YOU AVAILABLE IN THIS DATES"       
                list_date_most_match.append(value)
                list_attendace_most_match.append(dict_user_opinion)

            date_match[index] = value
            date_match["Interval "+index] = dict_user_opinion 

        if list_date_match is not None:
            date_match_interval = list_date_match[0]
            attendance_match = list_attendace_match[0]
            result = "ALL OF YOU CAN ATTEND IN THIS DATES"
        elif list_date_most_match is not None :
            date_match_interval = list_date_most_match
            attendance_match = list_attendance_most_match[0]
            result = "MOST OF YOU AVAILABLE IN THIS DATES"  
        else :
            date_match_interval = []   
            result = "DATES NOT FOUND"
        
        date_result = {'summary' : result,
                        'result' :{'date': date_match_interval,'attendance':attendance_match}}

        event_query = Events.query.get(event_id)
        event_query.start_date = date_match_interval[0]
        event_query.end_date = date_match_interval[-1]

        db.session.commit()

        return date_result, 200


class GetAllParticipantsEvent(Resource):
    """ Class to get all participant in Event """
    
    @jwt_required
    def get(self, event_id):
        """ 
        function to get participant in some event
        """

        '''
        get participant_id as creator_id
        '''
        event_query = Events.query.get(event_id)
        event = marshal(event_query, Events.response_fields)
        creator_id = event['creator_id']
        user_as_creator_query = Users.query.get(creator_id)
        user_as_creator = marshal(user_as_creator_query, Users.response_fields)
        creator_username = user_as_creator['username']
        creator_fullname = user_as_creator['fullname']

        creator_identity = {
            'id_participant': creator_id,
            'username': creator_username,
            'fullname': creator_fullname
        }

        '''
        get participant_id as invited
        '''
        list_of_participants = []
        participants_query = Invitations.query.filter_by(event_id = event_id)
        for participant in participants_query:
            participant_new = marshal(participant, Invitations.response_fields)
            participant_id = participant_new['invited_id']
            user_as_participant_query = Users.query.get(participant_id)
            user_as_participant = marshal(user_as_participant_query, Users.response_fields)
            dictionary_participant = {}
            dictionary_participant['id_participant'] = user_as_participant['user_id']
            dictionary_participant['username'] = user_as_participant['username']
            dictionary_participant['fullname'] = user_as_participant['fullname']
            list_of_participants.append(dictionary_participant)
        
        list_of_participants.append(creator_identity)

        return list_of_participants, 200, {'Content-Type' : 'application/json'}

class AllUserPreference(Resource):
    """
    class for getting all preference from participant
    """

    def get(self, event_id):
        """
        function to get all user preference in certain event
        """

        user_preferences_query = UserPreferences.query.filter_by(event_id=event_id)

        '''
        get every user_id, preference, and username in certain event
        '''
        list_of_user_preference = []
        for user_preference in user_preferences_query:
            dictionary_for_save_preference = {}
            user_preferences_new = marshal(user_preference, UserPreferences.response_fields)
            dictionary_for_save_preference['user_id'] = user_preferences_new['user_id']
            user_query = Users.query.get(user_preferences_new['user_id'])
            user = marshal(user_query, Users.response_fields)
            dictionary_for_save_preference['username'] = user['username']
            dictionary_for_save_preference['event_id'] = event_id
            dictionary_for_save_preference['preference'] = user_preferences_new['preference']
            list_of_user_preference.append(dictionary_for_save_preference)
        
        return list_of_user_preference, 200, {'Content-Type' : 'application/json'}


api.add_resource(EventsResource, '','/<event_id>')
api.add_resource(EventsOngoingResource, '/ongoing')
api.add_resource(EventsHistoryResource, '/history')
api.add_resource(EventsPreferenceResource, '/dominant_preference/<event_id>')
api.add_resource(EventsDatesGenerateResource, '/generate_date/<event_id>')
api.add_resource(GetAllParticipantsEvent, '/list_of_participant/<event_id>')
api.add_resource(AllUserPreference, '/all_user_preference/<event_id>')
