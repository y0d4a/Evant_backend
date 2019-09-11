import pytest, json, logging
from flask import Flask, request
from blueprints.users.model import Users
from blueprints.invitations.model import Invitations
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

    user = Users("mahar", "maharraden765@gmail.com", "agh765vx765", True, "Raden Panji", "Jombang", "082283511672")
    user2 = Users("raden", "radenraden765@gmail.com", "agh765vx765", True, "Raden Panji", "Jombang", "082283511673")
    invitation1 = Invitations(1, 1, 0)
    invitation2 = Invitations(2, 1, 0)

    # save users to database
    db.session.add(user)
    db.session.add(user2)
    db.session.add(invitation1)
    db.session.add(invitation2)
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