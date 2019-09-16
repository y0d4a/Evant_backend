from tests import app, client, cache, create_token, reset_database, create_token1, create_token2
import json

class TestInvitationsCrud():

    """
    class to test invitations resource
    """

    reset_database()

    def test_invitations_get_valid(self, client):
        token = create_token()
        res = client.get('/api/invitations',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_invitations_get_none(self, client):
        token = create_token2()
        res = client.get('/api/invitations',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_invitations_get_invalid_no_token(self, client):
        """
        test invalid get without token
        """

        res = client.get('/api/invitations',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_invitations_post_valid(self, client):
        token = create_token()
        data = {
            "invited_id": 5
        }
        res = client.post('/api/invitations', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_invitations_post_invalid_no_token(self, client):
        """
        test invalid post without token
        """
        
        data = {
            "event_id" : 3,
            "invited_id": 2
        }
        res = client.post('/api/invitations', data=json.dumps(data),
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_invitations_accept_valid(self, client):
        token = create_token()
        res = client.put('/api/invitations/accept/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_invitations_accept_invalid(self, client):
        token = create_token2()
        res = client.put('/api/invitations/accept/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 404:
            raise ValueError('The res.status_code must be 404, please check your code')
    
    def test_invitations_accept_invalid_no_token(self, client):
        """
        test invalid accept without token
        """
        
        res = client.put('/api/invitations/accept/1',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_invitations_reject_valid(self, client):
        token = create_token1()
        res = client.put('/api/invitations/reject/3',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_invitations_reject_invalid(self, client):
        token = create_token2()
        res = client.put('/api/invitations/reject/2',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 404:
            raise ValueError('The res.status_code must be 404, please check your code')
    
    def test_invitations_reject_invalid_no_token(self, client):
        """
        test invalid reject without token
        """
        
        res = client.put('/api/invitations/reject/2',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_invitations_user_decline_event(self, client):
        """
        test invalid reject without token
        """
        token = create_token()
        res = client.delete('/api/invitations/decline/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')    


    def test_invitations_user_invalid_decline_event(self, client):
        """
        test invalid reject without token
        """
        token = create_token2()
        res = client.delete('/api/invitations/decline/2',
                headers={'Authorization':'Bearer ' + token},
                content_type='application/json')

        if res.status_code != 404:
            raise ValueError('The res.status_code must be 404, please check your code')    
