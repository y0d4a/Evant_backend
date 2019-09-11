import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .model import AvailableDates
from flask_jwt_extended import get_jwt_identity, jwt_required
from blueprints import db, app

bp_available_dates = Blueprint("dates", __name__)
api = Api(bp_available_dates)

class DateResource (Resource):
    """Class for add date, delete date, and generate result date"""

    @jwt_required
    def post(self):
        """this function for add available dates to database"""

        identity = get_jwt_identity()
        user_id = identity['user_id']


        parser = reqparse.RequestParser()
        parser.add_argument('date', location='json')
        args = parser.parse_args()

        available_dates = AvailableDates(user_id, args['date'])
        db.session.add(available_dates)
        db.session.commit()
        
        app.logger.debug('DEBUG : %s', available_dates)

        return marshal(available_dates, AvailableDates.response_fields), 200, {'Content-Type' : 'application/json'}


    @jwt_required
    def delete(self):
        """this function for delete available date by id"""

        parser = reqparse.RequestParser()
        parser.add_argument('date', location='json')
        args = parser.parse_args()

        available_dates= AvailableDates.query.filter_by(date=args['date']).first()
        
        if available_dates is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(available_dates)
        db.session.commit()

        app.logger.debug('DEBUG : %s', available_dates)
        return {'status': 'DELETED'}, 200


    @jwt_required
    def get(self):
        """this function for marking calender depend on available dates"""

        identity = get_jwt_identity()
        user_id = identity['user_id']

        dates_query = AvailableDates.query.filter_by(user_id=user_id)
        dates = []
        
        for date in dates_query.all():
            dates.append(marshal(date, AvailableDates.response_fields))

        app.logger.debug('DEBUG : %s', dates_query)
        
        return dates, 200, {'Content-Type': 'application/json'}

api.add_resource(DateResource, '')