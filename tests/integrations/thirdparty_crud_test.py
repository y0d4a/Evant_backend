from tests import app, client, cache, create_token, reset_database
from blueprints.third_party import RecommendationPlaceToEat, RecommendationPlaceToHike, RecommendationPlaceToVacation
import json
from mock import patch

class TestThirdPartyCrud():
    """class to test third party api"""

    reset_database()
    def test_zomato_get_valid(self, client):
        """class to test third party api zomato"""

        token = create_token()
        res = client.get('/api/recommendation/eat/2',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    

    def test_vacation_get_valid(self, client):
        """class to test third party api vacation"""

        token = create_token()
        res = client.get('/api/recommendation/vacation/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_hiking_get_valid(self, client):
        """class to test third party api zomato"""

        token = create_token()
        res = client.get('/api/recommendation/hiking/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')


    @patch.object(RecommendationPlaceToEat, 'get')
    def testGetZomatoMock(self, mock_get):
        """class to test third party api zomato with mock"""
        response =  {
        "restaurants": "WAKI Japanese BBQ Dining",
        "address": "Lantai 1, Jl. Tanjung Karang No. 5, Thamrin, Jakarta",
        "photo": "https://b.zmtcdn.com/data/reviews_photos/621/2623a19855d87924b3e4271473d8c621_1566921104.jpg?fit=around%7C200%3A200&crop=200%3A200%3B%2A%2C%2A"}
        
        mock_get.return_value = response

        assert RecommendationPlaceToEat.get('https://developers.zomato.com/api/v2.1/search?b875502a178dcc62abd9f3437d92fbe5') == response
    
    @patch.object(RecommendationPlaceToVacation, 'get')
    def testGetVacationMock(self, mock_get):
        """class to test third party api vacation with mock"""
        
        response =  {
        "place": "Candi Borobudur",
        "place_location": "Magelang",
        "photo": "https://b.zmtcdn.com/data/reviews_photos/621/2623a19855d87924b3e4271473d8c621_1566921104.jpg?fit=around%7C200%3A200&crop=200%3A200%3B%2A%2C%2A"}
        
        mock_get.return_value = response

        assert RecommendationPlaceToVacation.get('https://opentripmap-places-v1.p.rapidapi.com/en/places/bbox?lon_min=107&lon_max=113&lat_min=-7&lat_max=-2') == response
    
    @patch.object(RecommendationPlaceToHike, 'get')
    def testGetHikingMock(self, mock_get):
        """class to test third party api hiking with mock"""
        
        response =  {
        "place": "Gunung Salak",
        "place_location": "Bogor",
        "photo": "https://b.zmtcdn.com/data/reviews_photos/621/2623a19855d87924b3e4271473d8c621_1566921104.jpg?fit=around%7C200%3A200&crop=200%3A200%3B%2A%2C%2A"}
        
        mock_get.return_value = response

        assert RecommendationPlaceToHike.get('https://opentripmap-places-v1.p.rapidapi.com/en/places/bbox?lon_min=107&lon_max=113&lat_min=-7&lat_max=-2') == response
    