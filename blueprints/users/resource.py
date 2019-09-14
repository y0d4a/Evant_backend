import json
import re
from passlib.hash import sha256_crypt
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Users

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt_claims

from blueprints import db, app

bp_user = Blueprint('users', __name__)
api = Api(bp_user)


class UserRequest(Resource):

    """ 
    Class for standard user action GET, PUT 
    """

    def get(self):

        """ 
        method request to get all users
        """
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

        """ 
        method to edit user profile 
        """
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

    """
    class for user login for getting authentication
    """

    def post(self):

        """
        method to get token 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True, help = "Your input username is invalid")
        parser.add_argument('password', location='json', required=True, help = "Your input password is invalid")
        args = parser.parse_args()
        
        user_query = Users.query.filter_by(username=args['username']).first()
        user = marshal(user_query, Users.response_fields)

        '''
        verify user login password
        '''
        verify_password = sha256_crypt.verify(args['password'], user['password'])

        if user_query is not None:
            if verify_password:
                '''
                get token for login
                '''
                identity_jwt = Users.query.filter_by(username=args['username']).first()
                user_identity = marshal(identity_jwt, Users.jwt_response_fields)
                token = create_access_token(identity=user_identity)

                return {'token': token, "user":user_identity}, 200, {'Content-Type' : 'application/json'}
        else:
            return {'status': 'FAILED USERNAME', 'message': 'please cek the correctness of your password'}, 401
        
        return {'status': 'INVALID PASSWORD', 'message': 'please cek the correctness of your password'}, 401


class UserRefreshToken(Resource):

    """
    class for refresh token for auth
    """

    @jwt_required
    def post(self):

        """
        method to refresh token
        """
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token': token}, 200, {'Content-Type' : 'application/json'}


class UserMakeRegistration(Resource):

    """
    class for user to create account (register)
    """

    def post(self):

        """ 
        method to make his/her account
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True, help="please add your username")
        parser.add_argument('email', location='json', required=True, help = "You did not fill your password")
        parser.add_argument('password', location='json', required=False)
        parser.add_argument('gender', location='json', required=False, type = inputs.boolean)
        parser.add_argument('fullname', location='json', required=False)
        parser.add_argument('address', location='json', required=False)
        parser.add_argument('phone', location='json', required=False)
        args = parser.parse_args()

        password = sha256_crypt.encrypt(args['password'])

        '''
        for email validation
        '''
        pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        result = re.match(pattern, args['email'])
        
        status_first_login = True
        if result:
            user = Users(args['username'], args['email'], password, args['gender'], status_first_login, args['fullname'], args['address'], args['phone'])
            db.session.add(user)
            db.session.commit()

            app.logger.debug('DEBUG : %s', user)

            return marshal(user, Users.response_fields), 200, {'Content-Type' : 'application/json'}   
        else:
            return "Your Email is Invalid", 400

class UserForgotPassword(Resource):

    """
    class for user to make new password
    """

    def post(self):

        """
        method to add new password
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True, help = "Your input email is invalid")
        parser.add_argument('new_password', location='json', required=True, help = "Your input password is invalid")
        args = parser.parse_args()
        
        pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        result = re.match(pattern, args['email'])
        
        if result:
            user_query = Users.query.filter_by(email=args['email']).first()
        
            '''
            add the new user password to database
            '''
            if user_query is not None:
                password = sha256_crypt.encrypt(args['new_password'])
                user_query.password = password
                db.session.commit()
                return {'status': 'NEW PASSWORD HAS ADDED'}, 200
            else:
                return {'status': 'FAILED USERNAME', 'message': 'please cek the correctness of your password'}, 401
        
            return {'status': 'INVALID PASSWORD AND USERNAME', 'message': 'please cek the correctness of your password and username'}, 401
        
        else:
            return "Your Input Email Has Been Wrong", 400

class AfterUserFirstLogin(Resource):

    """"
    class for change the user first login status
    """"

    @jwt_required
    def get(self):

        '''
        method to change user first login status
        '''
        user = get_jwt_identity()
        user_query = Users.query.get(user['user_id'])

        user_query.status_first_login = False

        db.session.commit()

        return marshal(user_query, Users.response_fields), 200, {'Content-Type' : 'application/json'}

class UserLoginWithGoogle(Resource):

    '''
    class for user to login with google
    '''

    def post(self):

        """
        method to verify token auth for login
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True, help = "Your input username is invalid")
        parser.add_argument('token_google', location='json', required=True, help = "Your input password is invalid")
        args = parser.parse_args()

        '''
        create jwt_authentication with google token
        '''
        if args['email'] is not None:
            if args['token_google']:
                '''
                get token for login
                '''
                identity_jwt = Users.query.filter_by(email=args['email']).first()
                user_identity = marshal(identity_jwt, Users.jwt_response_fields)
                token = create_access_token(identity=user_identity)

                return {'token': token, "user":user_identity}, 200, {'Content-Type' : 'application/json'}
        else:
            return {'status': 'FAILED EMAIL', 'message': 'please cek the correctness of your password'}, 401
        
        return {'status': 'INVALID TOKEN', 'message': 'please cek the correctness of your request'}, 401

class UserRegisterWithGoogle(Resource):

    """
    class for creating account (register)
    """

    def post(self):

        """
        method for User to make account
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True, help="please add your username")
        parser.add_argument('email', location='json', required=True, help = "You did not fill your password")
        parser.add_argument('password', location='json', required=False)
        parser.add_argument('gender', location='json', required=False, type = inputs.boolean)
        parser.add_argument('fullname', location='json', required=False)
        parser.add_argument('address', location='json', required=False)
        parser.add_argument('phone', location='json', required=False)
        args = parser.parse_args()

        password = sha256_crypt.encrypt(args['password'])

        '''
        for email validation
        '''
        pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        result = re.match(pattern, args['email'])
        
        status_first_login = True
        if result:
            user = Users(args['username'], args['email'], password, args['gender'], status_first_login, args['fullname'], args['address'], args['phone'])
            db.session.add(user)
            db.session.commit()

            app.logger.debug('DEBUG : %s', user)

        else:
            return "Invalid Email", 400

        if args['email'] is not None:
            '''
            get token for login
            '''
            identity_jwt = Users.query.filter_by(email=args['email']).first()
            user_identity = marshal(identity_jwt, Users.jwt_response_fields)
            token = create_access_token(identity=user_identity)

            return {'token': token, "user":user_identity}, 200, {'Content-Type' : 'application/json'}
        else:
            return "Invalid Email", 400        


api.add_resource(UserRequest, '', '/<id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRefreshToken, '/refresh')
api.add_resource(UserMakeRegistration, '/register')
api.add_resource(AfterUserFirstLogin, '/after_first_login')
api.add_resource(UserLoginWithGoogle, '/google_login')
api.add_resource(UserForgotPassword, '/add_new_password')
api.add_resource(UserRegisterWithGoogle, '/register_with_google')

