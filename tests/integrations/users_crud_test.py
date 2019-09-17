import json
from tests import app, client, cache, create_token, reset_database, create_token1

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
            'username':'nandom',
            'email':'nandommaharjo@gmail.com',
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
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_users_login(self, client):
        data = {
            'username':'ranum',
            'password':'agh765vx765',
        }

        res = client.post('/api/users/login', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_users_invalid_login_credential(self, client):
        """ test invalid POST with bad request 401 """
        
        data = {
            'username':'ranum',
            'password':'agh765vadsadsadsax765',
        }

        res = client.post('/api/users/login', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_users_invalid_login(self, client):
        """ test invalid POST with bad request 400 """
        
        data = {
            'password':'agh765vx765',
        }

        res = client.post('/api/users/login', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 400:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_users_post(self, client):
        data = {
            'username':'radani',
            'email':'panji@alterra.id',
            'password':'vxvxvx',
            'gender':False,
            'fullname':'radina yeah',
            'address':'jombang',
            'phone':'08222221565637'
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

        res = client.post('/api/users/register', data=json.dumps(data))
        
        assert res.status_code == 400
        # if res.status_code != 400:
            # raise ValueError('The res.status_code must be 400, please check your code')
    
    def test_users_after_login(self, client):
        token = create_token1()

        res = client.get('/api/users/after_first_login', headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_users_after_login_invalid(self, client):
        token = create_token1()

        res = client.get('/api/users/after_first_login',
                        content_type='application/json')
        
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_users_post_forgot_password(self, client):
        data = {
            'email':'panji@alterra.id',
            'new_password':'vxvxvx'
        }

        res = client.post('/api/users/add_new_password', data=json.dumps(data),
                        content_type='application/json')
        
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_users_post_forgot_password_invalid_email(self, client):
        data = {
            "email":"anasoas@alterra.id",
            "new_password":"vxvxvx"
        }

        res = client.post('/api/users/add_new_password', data=json.dumps(data),
                        content_type='application/json')

        assert res.status_code == 401
        # if res.status_code != 401:
        #     raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_users_post_forgot_password_invalid_email(self, client):
        data = {
            'new_password':'vxvxvx'
        }

        res = client.post('/api/users/add_new_password', data=json.dumps(data),
                        content_type='application/json')
        
        assert res.status_code == 400

    def test_users_post_google_login(self, client):
        data = {
            "email":"panji@alterra.id",
            "token_google":"vxvxvx"
        }

        res = client.post('/api/users/google_login', data=json.dumps(data),
                        content_type='application/json')

        assert res.status_code == 200
    
    def test_users_post_google_login_invalid_email(self, client):
        data = {
            "email":"panasji@alterra.id",
            "token_google":"vxvxvx"
        }

        res = client.post('/api/users/google_login', data=json.dumps(data),
                        content_type='application/json')

        assert res.status_code == 401
    
    def test_users_post_google_registration(self, client):
        data = {
            'username':'nanda',
            'email':'maharraden765@gmail.com',
            'password':'vxvxvx',
            'gender':False,
            'fullname':'radina yeah',
            'address':'jombang',
            'phone':'08222221565637'
        }

        res = client.post('/api/users/register_with_google', data=json.dumps(data),
                        content_type='application/json')

        assert res.status_code == 200
    
    def test_users_post_google_registration_invalid(self, client):
        data = {
            'username':'nandaasa',
            'email':'maharraden765gmail.com',
            'password':'vxvxvx',
            'gender':False,
            'fullname':'radina yeah',
            'address':'jombang',
            'phone':'08222221565637'
        }

        res = client.post('/api/users/register_with_google', data=json.dumps(data),
                        content_type='application/json')

        assert res.status_code == 400


    