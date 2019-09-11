from tests import app, client, cache, create_token, reset_database
import json

class TestCategoriesCrud():
    """class to test dates resource"""

    reset_database()

    def test_categories_post_valid(self, client):
        token = create_token()
        data = {
            "preference": "pedas",
            "category":"makan"
        }
        res = client.post('/api/category', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_categories_post_invalid_no_token(self, client):
        """test invalid post without token"""
        
        data = {
            "preference": "pedas",
            "category":"makan"
        }
        res = client.post('/api/category', data=json.dumps(data),
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_categories_get_valid(self, client):
        token = create_token()
        data = {
            "category":"makan"
        }
        res = client.get('/api/category', query_string=data,
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_categories_get_invalid_no_token(self, client):
        """test invalid post without token"""
        
        data = {
            "category":"makan"
        }
        res = client.get('/api/category', query_string=data,
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')