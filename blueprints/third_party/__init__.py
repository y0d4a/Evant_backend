import requests
import json
import operator
import random
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.user_preferences.model import UserPreferences
from blueprints.events.model import Events

from blueprints import db, app

bp_third_party = Blueprint('third_party',__name__)
api = Api(bp_third_party)

class RecommendationPlaceToEat(Resource):

    """
    Class to get recommendation place depend on user preference
    """

    '''
    Zomato host and api key
    '''
    zmt_host = 'https://developers.zomato.com/api/v2.1'
    zmt_apikey = 'b875502a178dcc62abd9f3437d92fbe5'

    @jwt_required
    def get(self,event_id = None):

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

        '''
        Generate Zomato API to get place recommendation
        '''
        location_request = requests.get(self.zmt_host + '/locations', params={'query':'jakarta'},headers={'user-key': self.zmt_apikey})
        geo = location_request.json()
        latitude  = geo['location_suggestions'][0]['latitude']
        longitude  = geo['location_suggestions'][0]['longitude']

        zomato_request = requests.get(self.zmt_host + '/search', params={'lat': latitude, 'lon': longitude, 'category':dominant_preference}, headers={'user-key' : self.zmt_apikey})
        restaurants = zomato_request.json()

        restaurant_count = len(restaurants['restaurants'])
        idx_restaurant = list(range(0,restaurant_count))
        restaurant_show = random.sample(idx_restaurant,3)

        restaurant_list = []

        for restaurant in restaurant_show:
            response_dummy = {
                'place' : restaurants['restaurants'][restaurant]['restaurant']['name'],
                'place_location' : restaurants['restaurants'][restaurant]['restaurant']['location']['address'],
                'photo' : restaurants['restaurants'][restaurant]['restaurant']['photos'][0]['photo']['thumb_url']
            }
            restaurant_list.append(response_dummy)
        
        event_query = Events.query.get(event_id)
        event_query.preference = dominant_preference
        db.session.commit()

        return restaurant_list, 200, {'Content-Type' : 'application/json'}


class RecommendationPlaceToVacation(Resource):

    """
    Class to get recommendation place depend on user preference
    """

    '''
    Open trip host and api key
    '''
    holiday_host = 'https://opentripmap-places-v1.p.rapidapi.com/en/places/bbox'
    photo_holiday_host = 'https://opentripmap-places-v1.p.rapidapi.com/en/places/xid/'
    holiday_key = 'd8dbe8efcfmsh22520433e8bc04fp138102jsnb6ebeee18548'


    @jwt_required
    def get(self,event_id = None):

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

        '''
        Generate Location API to get place recommendation
        '''
        location_host = 'https://api.opencagedata.com/geocode/v1/json'
        location_key = '27c217069e864fc4a6af09e706428fed'

        location_request = requests.get(location_host, params={'q':dominant_preference, 'key':location_key})
        geo = location_request.json()   
        latitude  = geo['results'][0]['bounds']['southwest']['lat']
        longitude = geo['results'][0]['bounds']['southwest']['lng']

        latitude = int(latitude)
        latitude_min = latitude - 2
        latitude_max = latitude + 2

        longitude = int(longitude)
        longitude_min = longitude - 2
        longitude_max = longitude + 2
        
        vacation_request = requests.get(self.holiday_host, params={'lon_min':longitude_min, 'lon_max': longitude_max, 'lat_min': latitude_min, 'lat_max':latitude_max}, headers={'x-rapidapi-key' : self.holiday_key})

        vacations = vacation_request.json()


        vacation_list = []

        for vacation in range(3):
            xid = vacations['features'][vacation]['properties']['xid']  
            photo_request = requests.get(self.photo_holiday_host+ str(xid), headers={'x-rapidapi-key' : self.holiday_key})
            photo = photo_request.json()
            print(photo)
            response_dummy = {
                'place' : vacations['features'][vacation]['properties']['name'],
                'place_location' : dominant_preference,
                'photo' : photo['preview']['source']
            }

            vacation_list.append(response_dummy)
        
        event_query = Events.query.get(event_id)
        event_query.preference = dominant_preference
        db.session.commit()

        return vacation_list, 200, {'Content-Type' : 'application/json'}
  
    
class RecommendationPlaceToHike(Resource):

    """
    Class to get recommendation hiking place depend on user preference
    """

    '''
    Hikingproject host and api key
    '''
    hiking_host = 'https://www.hikingproject.com/data/get-trails'
    hiking_key = '200590840-81a8541f9a61f725af8793b6d29cf8bb'

    @jwt_required
    def get(self,event_id = None):

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

        '''
        Generate Hiking API to get place recommendation
        '''
        location_host = 'https://api.opencagedata.com/geocode/v1/json'
        location_key = '27c217069e864fc4a6af09e706428fed'

        location_request = requests.get(location_host, params={'q':dominant_preference, 'key':location_key})
        geo = location_request.json()

        latitude  = geo['results'][0]['bounds']['southwest']['lat']
        longitude = geo['results'][0]['bounds']['southwest']['lng']
        maxDistance = 200
        
        hiking_request = requests.get(self.hiking_host, params={'lat': latitude, 'lon': longitude, 'maxDistance': maxDistance, 'key':self.hiking_key})
        hikings = hiking_request.json()

        hiking_count = len(hikings['trails'])
        idx_hiking = list(range(0,hiking_count))
        hiking_show = random.sample(idx_hiking,3)
        
        hiking_list = []

        for hiking in hiking_show:    
            response_dummy = {
                'place' : hikings['trails'][hiking]['name'],
                # 'place_location' : dominant_preference,
                'photo' : hikings['trails'][hiking]['imgMedium']
            }

            hiking_list.append(response_dummy)

        event_query = Events.query.get(event_id)
        event_query.preference = dominant_preference
        db.session.commit()
    
        return hikings, 200, {'Content-Type' : 'application/json'}


api.add_resource(RecommendationPlaceToEat,'/eat/<event_id>','/eat')
api.add_resource(RecommendationPlaceToVacation,'/vacation/<event_id>','/vacation')
api.add_resource(RecommendationPlaceToHike,'/hiking/<event_id>','/hiking')
