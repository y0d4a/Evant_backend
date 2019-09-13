import json
import re
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Users

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt_claims

from blueprints import db, app, bcrypt

bp_user = Blueprint('users', __name__)
api = Api(bp_user)


class UserRequest(Resource):
    """ Standart user action GET, PUT """

    def get(self):
        """ Request to Get All users """

        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', required = False, default = 1)
        parser.add_argument('rp', type = int, location = 'args', required = False, default = 25)
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        user_qry = Users.query

        user_qry= user_qry.limit(args['rp']).offset(offset).all()
        list_temporary = []

        for row in user_qry:
            list_temporary.append(marshal(row, Users.jwt_response_fields))
        
        return list_temporary, 200, {'Content-Type' : 'application/json'}

    def put(self, id):
        """ User request for editing his/her biodata """

        parser = reqparse.RequestParser()
        parser.add_argument('username', location ='json', required=False)
        parser.add_argument('email', location='json', required=False)
        parser.add_argument('password', location = 'json', required=False)
        parser.add_argument('gender', location = 'json', required=False, type = inputs.boolean)
        parser.add_argument('status_first_login', location = 'json', required=False, type = inputs.boolean)
        parser.add_argument('fullname', location = 'json', required=False)
        parser.add_argument('address', location = 'json', required=False)
        parser.add_argument('phone', location = 'json', required=False)
        args = parser.parse_args()

        user_qry = Users.query.get(id)

        if user_qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        if args['username'] is not None:
            user_qry.username = args['username']
        if args['email'] is not None:
            user_qry.email = args['email']
        if args['password'] is not None:
            user_qry.password = args['password']
        if args['gender'] is not None:
            user_qry.gender = args['gender']
        if args['fullname'] is not None:
            user_qry.fullname = args['fullname']
        if args['address'] is not None:
            user_qry.address = args['address']
        if args['status_first_login'] is not None:
            user_qry.status_first_login = args['status_first_login']
        if args['phone'] is not None:
            user_qry.phone = args['phone']

        db.session.commit()

        return marshal(user_qry, Users.jwt_response_fields), 200, {'Content-Type' : 'application/json'}
    

class UserLogin(Resource):
    """ User login for getting authentication """

    def post(self):
        """ user ask token auth for login """

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True, help = "Your input username is invalid")
        parser.add_argument('password', location='json', required=True, help = "Your input password is invalid")
        args = parser.parse_args()


        user_query = Users.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        user = marshal(user_query, Users.jwt_response_fields)

        if user_query is not None:
            token = create_access_token(identity=user)
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        return {'token': token, "user":user}, 200, {'Content-Type' : 'application/json'}


class UserRefreshToken(Resource):
    """ User refresh token for auth """

    @jwt_required
    def post(self):
        """ user ask renewable token """
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token': token}, 200, {'Content-Type' : 'application/json'}


class UserMakeRegistration(Resource):
    """ User create account (register) """

    def post(self):
        """ User make his/her account """
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('gender', location='json', required=True, type = inputs.boolean)
        parser.add_argument('fullname', location='json', required=False)
        parser.add_argument('address', location='json', required=False)
        parser.add_argument('phone', location='json', required=False)
        args = parser.parse_args()

        pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        result = re.match(pattern, args['email'])
        
        status_first_login = True
        if result:

            user = Users(args['username'], args['email'], args['password'], args['gender'], status_first_login, args['fullname'], args['address'], args['phone'])
            db.session.add(user)
            db.session.commit()

            app.logger.debug('DEBUG : %s', user)

            return marshal(user, Users.response_fields), 200, {'Content-Type' : 'application/json'}
        else:
            return "Your Input Email Has Been Wrong", 400

class AfterUserFirstLogin(Resource):
    '''
    class for change the user first login status
    '''

    @jwt_required
    def get(self):
        '''
        function to change user first login status
        '''
        user = get_jwt_identity()
        user_query = Users.query.get(user['user_id'])

        user_query.status_first_login = False

        db.session.commit()

        return marshal(user_query, Users.response_fields), 200, {'Content-Type' : 'application/json'}



api.add_resource(UserRequest, '', '/<id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRefreshToken, '/refresh')
api.add_resource(UserMakeRegistration, '/register')
api.add_resource(AfterUserFirstLogin, '/after_first_login')
