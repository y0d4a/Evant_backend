import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .model import UserPreferences
from flask_jwt_extended import get_jwt_identity, jwt_required
from blueprints import db, app

bp_user_preferences = Blueprint('user_preferences', __name__)
api = Api(bp_user_preferences)


class UserPreferencesResources (Resource) :
    """POST and GET every user preferences"""

    @jwt_required
    def post(self):
        """Input user preferences to certain event_id"""	

        identity = get_jwt_identity()
        user_id = claims['user_id']
       

        parser = reqparse.RequestParser()
        parser.add_argument('event_id', location='json', required=True)
        parser.add_argument('preference', location='json', required=True)

        args = parser.parse_args()

        user_preferences = UserPreferences(user_id,args['event_id'],args['preference'])
        db.session.add(user_preferences)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_preferences)

        return marshal(user_preferences, UserPreferences.response_fields), 200, {
            'Content-Type': 'application/json'
        }


    @jwt_required
    def get(self,event_id):
        """Get all user preferences from certain event_id"""			

        user_preferences = UserPreferences.query
        preferences_event = user_preferences.filter_by(event_id=event_id)
        preferences = []
        
        for preference in preferences_event.all():
            preferences.append(marshal(preference, UserPreferences.response_fields))

        app.logger.debug('DEBUG : %s', user_preferences)
        
        return preferences, 200, {'Content-Type': 'application/json'}


api.add_resource(UserPreferencesResources, '', '/<event_id>')