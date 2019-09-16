import json
from tests import app, client, cache, create_token, reset_database

class TestUserPreferencesCrud():

    """
    class to test user preferences resource
    """

    reset_database()

    def test_user_preferences_post_valid(self, client):
        token = create_token()
        data = {
            "event_id" : 1,
            "preference": "cultural"
        }
        res = client.post('/api/users/preferences', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_user_preferences_post_invalid_no_token(self, client):
        data = {
            "event_id" : 1,
            "preference": "hambar"
        }
        res = client.post('/api/users/preferences', data=json.dumps(data),
                        content_type='application/json')
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_user_preferences_get_valid(self, client):
        token = create_token()
        res = client.get('/api/users/preferences/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_user_preferences_get_invalid_no_token(self, client):
        res = client.get('/api/users/preferences/1',
                        content_type='application/json')
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    
    def test_user_preferences_put_valid(self, client):
        token = create_token()
        data = {
            "preference": "dinner"
        }
        res = client.put('/api/users/preferences/1', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_user_preferences_put_invalid_token(self, client):
        data = {
            "preference": "dinner"
        }
        res = client.put('/api/users/preferences/1', data=json.dumps(data),
                        content_type='application/json')
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_user_get_confirmation_valid(self, client):
        token = create_token()
        res = client.get('/api/users/preferences/confirmations/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_user_get_confirmation_no_token(self, client):
        res = client.get('/api/users/preferences/confirmations/1',
                        content_type='application/json')
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_user_preferences_put_confirmation_valid(self, client):
        token = create_token()
        data = {
            "confirmation" : 1
        }
        res = client.put('/api/users/preferences/confirmations/1', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    

    def test_user_preferences_put_confirmation_invalid_no_token(self, client):
        data = {
            "confirmation" : 1
        }
        res = client.put('/api/users/preferences/confirmations/1', data=json.dumps(data),
                        content_type='application/json')
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')