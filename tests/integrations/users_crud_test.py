import json
from tests import app, client, cache, create_token, reset_database

class TestUsersCrud():
    """Test all request in users resource"""

    '''reset all database before testing'''
    reset_database()
    
    def test_users_get(self, client):
        token = create_token()
        res = client.get('/api/users', content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code!')
    
    def test_users_put(self, client):
        data = {
            'username':'ranpa',
            'email':'radenmaharjo@gmail.com',
            'password':'123456',
            'gender':False,
            'fullname':'Agatha Ranpa',
            'address':'blitar-jombang',
            'phone':'0822222137'
        }

        res = client.put('/api/users/1', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_users_invalid_put(self, client):
        """ test invalid PUT with bad request 404 """
     
        data = {
            'username':'mabar',
            'email':'makan@gmail.com',
            'password':'123456',
            'gender':False,
            'fullname':'Agatha',
            'address':'blitar-jombang',
            'phone':'0822222137'
        }

        res = client.put('/api/users/7', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 404:
            raise ValueError('The res.status_code must be 404, please check your code')

    def test_users_login(self, client):
        data = {
            'username':'ranpa',
            'password':'123456',
        }

        res = client.post('/api/users/login', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_users_invalid_login(self, client):
        """ test invalid POST with bad request 401 """
        
        data = {
            'username':'ranpa16',
            'password':'123456',
        }

        res = client.post('/api/users/login', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_users_post(self, client):
        data = {
            'username':'radani',
            'email':'panji@alterra.id',
            'password':'vxvxvx',
            'gender':False,
            'fullname':'radina yeah',
            'address':'jombang',
            'phone':'0822222137'
        }

        res = client.post('/api/users/register', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_users_invalid_post(self, client):
        """ test invalid POST with bad request 400 """

        data = {
            'username':'radanu',
            'password':'vxvxvx',
            'gender':False,
            'fullname':'radina yeah'
        }

        res = client.post('/api/users/register', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 400:
            raise ValueError('The res.status_code must be 400, please check your code')