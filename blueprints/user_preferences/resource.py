import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .model import UserPreferences
from blueprints.events.model import Events
from blueprints.users.model import Users
from flask_jwt_extended import get_jwt_identity, jwt_required
from blueprints import db, app

bp_user_preferences = Blueprint('user_preferences', __name__)
api = Api(bp_user_preferences)


class UserPreferencesResources (Resource) :

    """
    class for POST and GET every user preferences
    """

    @jwt_required
    def post(self):

        """
        method to input user preferences to certain event
        """	
        identity = get_jwt_identity()
        user_id = identity['user_id']

        parser = reqparse.RequestParser()
        parser.add_argument('event_id', location='json', required=True)
        parser.add_argument('preference', location='json', default="null")

        args = parser.parse_args()

        user_preferences = UserPreferences(user_id,args['event_id'],args['preference'])
        db.session.add(user_preferences)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_preferences)

        return marshal(user_preferences, UserPreferences.response_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def put(self,event_id):

        """
        method to edit user preferences to certain event
        """	
        identity = get_jwt_identity()
        user_id = identity['user_id']

        parser = reqparse.RequestParser()
        parser.add_argument('preference', location='json')

        args = parser.parse_args()

        preference_query = UserPreferences.query.filter_by(event_id=event_id, user_id=user_id).first()

        preference_query.preference = args['preference']
        db.session.commit()

        app.logger.debug('DEBUG : %s', preference_query)

        return marshal(preference_query, UserPreferences.response_fields), 200, {'Content-Type': 'application/json'}



    @jwt_required
    def get(self,event_id):

        """
        method to get all user preferences from certain event
        """			
        user_preferences = UserPreferences.query
        preferences_event = user_preferences.filter_by(event_id=event_id)
        preferences = []
        
        for preference in preferences_event.all():
            preferences.append(marshal(preference, UserPreferences.response_fields))

        app.logger.debug('DEBUG : %s', user_preferences)
        
        return preferences, 200, {'Content-Type': 'application/json'}

class ConfirmationResources(Resource):
    @jwt_required
    def get(self, event_id):
        identity = get_jwt_identity()
        user_id = identity['user_id']

        current_event = Events.query.get(event_id)

        '''get event confirmation status'''
        confirmations = UserPreferences.query.filter_by(event_id=event_id).all()

        result = []

        '''convenient output'''
        for confirmation in confirmations:
            current_user = Users.query.get(confirmation.user_id)
            temp = {
                'confirmation': confirmation.confirmation,
                'username':current_user.username,
                'fullname':current_user.fullname,
                'preference':confirmation.preference,
                'user_id':current_user.user_id
            }
            result.append(temp)

        return result, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self,event_id):

        """
        method to edit user preferences to certain event
        """	
        identity = get_jwt_identity()
        user_id = identity['user_id']

        parser = reqparse.RequestParser()
        parser.add_argument('confirmation', location='json', type=int, required=True)

        args = parser.parse_args()

        preference_query = UserPreferences.query.filter_by(event_id=event_id, user_id=user_id).first()

        preference_query.confirmation = args['confirmation']
        db.session.commit()

        app.logger.debug('DEBUG : %s', preference_query)

        return marshal(preference_query, UserPreferences.response_fields), 200, {'Content-Type': 'application/json'}



api.add_resource(UserPreferencesResources, '', '/<event_id>')
api.add_resource(ConfirmationResources, '/confirmations/<event_id>')
