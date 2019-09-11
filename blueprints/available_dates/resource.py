import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .model import AvailableDates
from flask_jwt_extended import get_jwt_claims, jwt_required
from blueprints import db

bp_available_dates = Blueprint('available_dates', __name__)
api = Api(bp_available_dates)

class DateResource (Resource):
    """Class for add date, delete date, and generate result date""""
    
    @jwt_required
    def post(self):
        """this function for add available dates to database"""

        claims = get_jwt_claims()
        user_id = claims['id']

        parser = reqparse.RequestParser()
        parser.add_argument('date', location='json')
        args = parser.parse_args()

        available_dates = AvailableDates(user_id, args['date'])
        db.session.add(available_dates)
        db.session.commit()
        
         app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type' : 'application/json'}


    @jwt_required
    def delete(self, id):
        """this function for delete available date by id""""


        parser = reqparse.RequestParser()
        parser.add_argument('date', location='json')
        args = parser.parse_args()

        available_dates= AvailableDates.query.filter_by(date=args['date']).first()
        
        if available_dates is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(available_dates)
        db.session.commit()

        return {'status': 'DELETED'}, 200




    # @jwt_required
    # def get():

api.add_resource(DateResource, '')