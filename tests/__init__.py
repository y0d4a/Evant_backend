import pytest, json, logging
from flask import Flask, request
from blueprints.users.model import Users
from passlib.hash import sha256_crypt
from blueprints.invitations.model import Invitations
from blueprints.available_dates.model import AvailableDates
from blueprints.user_preferences.model import UserPreferences
from blueprints.events.model import Events

from blueprints import db, app 
from app import cache


def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def reset_database():

    db.drop_all()
    db.create_all()
    

    password = sha256_crypt.encrypt("agh765vx765")

    user = Users("mahar", "maharraden765@gmail.com", password, True, True, "Raden Panji", "Jombang", "082283511672")
    user2 = Users("ranum", "ranumraden765@gmail.com", password, True, True, "Raden Panji", "Jombang", "082283511673")
   
    invitation1 = Invitations(1, 1, 0)
    invitation2 = Invitations(2, 2, 0)
    invitation3 = Invitations(2, 1, 1)

    date = AvailableDates(1, '27/09/2019')
    db.session.add(date)
    date = AvailableDates(1, '28/09/2019')
    db.session.add(date)
    date = AvailableDates(2, '27/09/2019')
    db.session.add(date)
    date = AvailableDates(2, '28/09/2019')
    db.session.add(date)
    date = AvailableDates(2, '29/09/2019')
    db.session.add(date)

    user_preference = UserPreferences(1, 2, 'Dinner')
    db.session.add(user_preference)
    user_preference = UserPreferences(2, 2, 'Dinner')
    db.session.add(user_preference)
    user_preference = UserPreferences(2, 1, 'cultural')
    db.session.add(user_preference)
 


    event1 = Events(1, "LIBURAN", "jalan-jalan ke mall", "26/09/2019", "03/10/2019", 3, 0)
    event2 = Events(2, "MAKAN", "pingin makan-makan", "26/09/2019", "03/10/2019", 3, 0)

    # save users to database
    db.session.add(user)
    db.session.add(user2)
    db.session.add(invitation1)
    db.session.add(invitation2)
    db.session.add(event1)
    db.session.add(event2)
    db.session.commit()

def create_token():
    token = cache.get('test-token')
    if token is None:
        data = {
            'username' : 'mahar',
            'password' : 'agh765vx765'
        }
        # do request
        req = call_client(request)
        res = req.post('/api/users/login', data=json.dumps(data), content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

def create_token1():
    token = cache.get('test-token')
    if token is None:
        data = {
            'username' : 'ranum',
            'password' : 'agh765vx765'
        }
        # do request
        req = call_client(request)
        res = req.post('/api/users/login', data=json.dumps(data), content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token