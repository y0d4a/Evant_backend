import requests
import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from blueprints.events.model import Events

bp_third_party = Blueprint('third_party',__name__)
api = Api(bp_third_party)

class RecommendationPlaceToEat(Resource):
    """Class to get recommendation place depend on user preference"""

    zmt_host = 'https://developers.zomato.com/api/v2.1'
    zmt_apikey = 'b875502a178dcc62abd9f3437d92fbe5'

    @jwt_required
    def get(self,event_id = None):
        """Function to generate Zomato API to get place recommendation"""

        location_request = requests.get(self.zmt_host + '/locations', params={'query':'jakarta'},headers={'user-key': self.zmt_apikey})
        geo = location_request.json()
        latitude  = geo['location_suggestions'][0]['latitude']
        longitude  = geo['location_suggestions'][0]['longitude']

        event = Events.query.filter_by(event_id = event_id)
        preference = event['preference']

        zomato_request = requests.get(self.zmt_host + '/search', params={'lat': latitude, 'lon': longitude, 'category': category}, headers={'user-key' : self.zmt_apikey})
        restaurants = zomato_request.json()

        restaurant_list = []

        for restaurant in range(3):
            response_dummy = {
                'restaurants' : restaurants['restaurants'][restaurant]['restaurant']['name'],
                'address' : restaurants['restaurants'][restaurant]['restaurant']['location']['address'],
                'city' : restaurants['restaurants'][restaurant]['restaurant']['location']['city']
            }
            restaurant_list.append(response_dummy)
        return restaurant_list, 200, {'Content-Type' : 'application/json'}



class RecommendationPlaceToVacation(Resource):
    """Class to get recommendation place depend on user preference"""

    holiday_host = 'https://opentripmap-places-v1.p.rapidapi.com/en/places/bbox'
    photo_holiday_host = 'https://opentripmap-places-v1.p.rapidapi.com/en/places/xid/'
    holiday_key = 'd8dbe8efcfmsh22520433e8bc04fp138102jsnb6ebeee18548'


    @jwt_required
    def get(self,event_id = None):
        """Function to generate opentripmap API to get place recommendation"""

        location_host = 'https://api.opencagedata.com/geocode/v1/json'
        location_key = '27c217069e864fc4a6af09e706428fed'
        
        parser = reqparse.RequestParser()
        parser.add_argument('q',location='args', default=None)        
        args = parser.parse_args()

        location_request = requests.get(location_host, params={'q':args['q'], 'key':location_key})
        geo = location_request.json()   
        latitude  = geo['results'][1]['bounds']['northeast']['lat']
        longitude = geo['results'][1]['bounds']['northeast']['lng']

        latitude = int(latitude)
        latitude_min = latitude-2
        latitude_max = latitude+2

        longitude = int(longitude)
        longitude_min = longitude-2
        longitude_max = longitude+2

        # event = Events.query.filter_by(event_id = event_id)
        # preference = event['preference']
        preference = 'religion'
        
        vacation_request = requests.get(self.holiday_host, params={'lon_min':longitude_min, 'lon_max': longitude_max, 'lat_min': latitude_min, 'lat_max':latitude_max, 'kinds':preference}, headers={'x-rapidapi-key' : self.holiday_key})
        vacations = vacation_request.json()

        vacation_list = []

        for vacation in range(3):

            xid = vacations['features'][vacation]['properties']['xid']  
            photo_request = requests.get(self.photo_holiday_host+ str(xid), headers={'x-rapidapi-key' : self.holiday_key})
            photo = photo_request.json()
            response_dummy = {
                'place' : vacations['features'][vacation]['properties']['name'],
                'photo' : photo['image']
            }

            vacation_list.append(response_dummy)
        return vacation_list, 200, {'Content-Type' : 'application/json'}
  
    

class RecommendationPlaceToHike(Resource):
    """Class to get recommendation hiking place depend on user preference"""

    hiking_host = 'https://www.hikingproject.com/data/get-trails'
    hiking_key = '200588281-f2209cf68acd4bb04507af0f7f382bba'

    @jwt_required
    def get(self,event_id = None):
        """Function to generate opentripmap API to get place recommendation"""
        location_host = 'https://api.opencagedata.com/geocode/v1/json'
        location_key = '27c217069e864fc4a6af09e706428fed'
        
        parser = reqparse.RequestParser()
        parser.add_argument('q',location='args', default=None)        
        args = parser.parse_args()

        event = Events.query.filter_by(event_id = event_id)
        preference = event['preference']


        location_request = requests.get(location_host, params={'q':preference, 'key':location_key})
        geo = location_request.json()

        latitude  = geo['results'][1]['bounds']['northeast']['lat']
        longitude = geo['results'][1]['bounds']['northeast']['lng']
        maxDistance = 200
        
        hiking_request = requests.get(self.hiking_host, params={'lat': latitude, 'lon': longitude, 'maxDistance': maxDistance, 'key':self.hiking_key})
        hikings = hiking_request.json()
        hiking_list = []

        for hiking in range(len(hikings['trails'])):
            
            response_dummy = {
                'place' : hikings['trails'][hiking]['name'],
                'photo' : hikings['trails'][hiking]['imgMedium']
            }

            hiking_list.append(response_dummy)
        return hiking_list, 200, {'Content-Type' : 'application/json'}


api.add_resource(RecommendationPlaceToEat,'/eat/<event_id>','/eat')
api.add_resource(RecommendationPlaceToVacation,'/vacation/<event_id>','/vacation')
api.add_resource(RecommendationPlaceToHike,'/hiking/<event_id>','/hiking')
