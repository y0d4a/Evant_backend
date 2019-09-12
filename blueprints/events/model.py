from blueprints import db
from flask_restful import fields

class Events(db.Model):

    """ Events Table Database """

    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key = True)
    creator_id = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(100), nullable = False)
    event_name = db.Column(db.String(100), nullable = False)
    status = db.Column(db.Integer, nullable = False)
    place_name = db.Column(db.String(100), nullable = True)
    place_location = db.Column(db.String(100), nullable = True)
    start_date = db.Column(db.String(100), nullable = True)
    end_date = db.Column(db.String(100), nullable = True)
    start_date_parameter = db.Column(db.DateTime, nullable = True)   
    end_date_parameter = db.Column(db.DateTime, nullable = True)
    preference = db.Column(db.String(100), nullable = True)
    duration = db.Column(db.Integer, nullable = True)

    response_fields = {
        'event_id' : fields.Integer,
        'creator_id': fields.Integer,
        'category' : fields.String,
        'event_name': fields.String,
        'status': fields.Integer,
        'place_name': fields.String,
        'place_location': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
        'start_date_parameter': fields.String,
        'end_date_parameter': fields.String,
        'preference': fields.String,
        'duration': fields.Integer
    }

    def __init__(self, creator_id, category, event_name, status, place_name = None, place_location = None, start_date = None, end_date = None, start_date_parameter = None, end_date_parameter = None, preference = None, duration = None):
        self.creator_id = creator_id
        self.category = category
        self.event_name = event_name
        self.status = status
        self.place_name = place_name
        self.place_location = place_location
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_parameter = start_date_parameter
        self.end_date_parameter = end_date_parameter
        self.preference = preference
        self.duration = duration

    def __repr__(self):
        return '<Events %r>' % self.event_id