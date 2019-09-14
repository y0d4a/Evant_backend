import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from .model import Categories
from flask_jwt_extended import jwt_required
from blueprints import db, app

bp_categories = Blueprint("categories", __name__)
api = Api(bp_categories)


class CategoryResource (Resource):

    """Class for add preference category and get all preference category"""

    def post(self):

        """method to add preference category"""
        parser = reqparse.RequestParser()
        parser.add_argument('preference', location='json')
        parser.add_argument('category', location='json')
        args = parser.parse_args()

        category = Categories(args['preference'], args['category'])
        db.session.add(category)
        db.session.commit()
        
        app.logger.debug('DEBUG : %s', category)

        return marshal(category, Categories.response_fields), 200, {'Content-Type' : 'application/json'}
    
    @jwt_required
    def get(self):

        """method to get all category from certain preferences"""			
        parser = reqparse.RequestParser()
        parser.add_argument('category', type = str, location = 'args', required = True)
        args = parser.parse_args()

        categories_query = Categories.query.filter_by(category=args['category'])
        categories = []
      
        for category in categories_query.all():
            categories.append(marshal(category, Categories.response_fields))

        app.logger.debug('DEBUG : %s', categories_query)
        
        return categories, 200, {'Content-Type': 'application/json'}

api.add_resource(CategoryResource, '')