from blueprints import db
from flask_restful import fields

class Invitations(db.Model):
    '''
    class for invitations table
    '''

    __tablename__ = 'invitations'

    event_id = db.Column(db.Integer, primary_key=True)
    invited_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)

    response_fields = {
        'event_id':fields.Integer,
        'invited_id':fields.Integer,
        'status':fields.Integer
    }

    def __init__(self, event_id, invited_id, status):
        self.event_id = event_id
        self.invited_id = invited_id
        self.status = status
    
