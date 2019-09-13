import json
from tests import app, client, cache, create_token, reset_database

class TestEventCrud():
    """Test all request in event resource"""

    '''reset all database event testing'''
    reset_database()

    def test_event_postevent(self,client):
        token = create_token()
        data = {
	        "category": "LIBURAN",
	        "event_name" : "Pingin Liburan ke Bali",
	        "start_date_parameter": "2019/09/26",
	        "end_date_parameter": "2019/10/03",
	        "duration":3
        }

        res = client.post('/api/events', data=json.dumps(data), headers={'Authorization':'Bearer ' + token}, content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_event_invalid_postevent(self,client):
        data = {
	        "event_name" : "Pingin Liburan ke Bali"
        }

        res = client.post('/api/events', data=json.dumps(data), content_type='application/json')

        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401 please check your code')

    def test_events_get(self, client):
        token = create_token()
        res = client.get('/api/events/1',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_events_get_invalid(self, client):
        token = create_token()
        res = client.get('/api/events/1',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_event_put(self, client):
        token = create_token()
        data = {
	        "start_date_parameter": "2019/09/26",
	        "end_date_parameter": "2019/10/03",
	        "duration":2
        }
        res = client.put('/api/events/2', data=json.dumps(data), headers={'Authorization':'Bearer ' + token}, content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_event_put_invalid(self, client):
        token = create_token()
        data = {
	        "start_date_parameter": "2019/09/26",
	        "end_date_parameter": "2019/10/03",
	        "duration":2
        }
        res = client.put('/api/events/2', data=json.dumps(data), content_type='application/json')

        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_events_get_ongoingevent(self, client):
        token = create_token()
        res = client.get('/api/events/ongoing',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_events_get_ongoingevent_invalid(self, client):
        token = create_token()
        res = client.get('/api/events/ongoing',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_events_get_history(self, client):
        token = create_token()
        res = client.get('/api/events/history',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_events_get_history_invalid(self, client):
        token = create_token()
        res = client.get('/api/events/history',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_events_get_dominant_preference(self, client):
        token = create_token()
        res = client.get('/api/events/dominant_preference/2',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_events_get_dominant_preference_invalid(self, client):
        token = create_token()
        res = client.get('/api/events/dominant_preference/2',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_events_get_generate_date(self, client):
        token = create_token()
        res = client.get('/api/events/generate_date/2',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_events_get_generate_date_invalid(self, client):
        token = create_token()
        res = client.get('/api/events/generate_date/2',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')
    
    def test_events_get_all_user_preferences(self, client):
        token = create_token()
        res = client.get('/api/events/all_user_preference/2',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')
    
    def test_events_get_list_of_participant(self, client):
        token = create_token()
        res = client.get('/api/events/list_of_participant/2',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_events_get_list_of_participant_invalid(self, client):
        token = create_token()
        res = client.get('/api/events/list_of_participant/2',
                        content_type='application/json')
        res_json = json.loads(res.data)
        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')

    def test_event_delete(self, client):
        token = create_token()
        res = client.delete('/api/events/2',
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')

        if res.status_code != 200:
            raise ValueError('The res.status_code must be 200, please check your code')

    def test_event_delete(self, client):
        token = create_token()
        res = client.delete('/api/events/2',
                        content_type='application/json')

        if res.status_code != 401:
            raise ValueError('The res.status_code must be 401, please check your code')    
    