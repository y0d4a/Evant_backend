from tests import app, client, cache, create_token, reset_database
import json

class TestDatesCrud():
    """class to test dates resource"""

    reset_database()

    def test_dates_post_valid(self, client):
        token = create_token()
        data = {
            "date": "20-01-2020"
        }
        res = client.post('/api/date', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_dates_post_invalid_no_token(self, client):
        """test invalid post without token"""
        
        data = {
            "date": "11-12-2019"
        }
        res = client.post('/api/date', data=json.dumps(data),
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_dates_delete_valid(self, client):
        token = create_token()
        data = {
            "date": "20-01-2020"
        }
        res = client.delete('/api/date', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_dates_delete_invalid_no_token(self, client):
        """test invalid post without token"""
        
        data = {
            "date": "11-12-2019"
        }
        res = client.delete('/api/date', data=json.dumps(data),
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    