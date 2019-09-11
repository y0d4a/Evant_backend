from blueprints import db
from flask_restful import fields

class Events(db.Model):

    """ Events Table Database """

    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key = True, unique = True)
    creator_id = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(100), nullable = True)
    event_name = db.Column(db.String(100), nullable = True)
    place_name = db.Column(db.String(100), nullable = True)
    place_location = db.Column(db.String(100), nullable = True)
    start_date = db.Column(db.String(100), nullable = True)
    end_date = db.Column(db.String(100), nullable = True)
    start_date_parameter = db.Column(db.String(100), nullable = False)   
    end_date_parameter = db.Column(db.String(100), nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Integer, nullable = True )

    response_field = {
        'event_id' : fields.Integer,
        'creator_id': fields.Integer,
        'category' : fields.String,
        'event_name': fields.String,
        'place_name': fields.String,
        'place_location': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
        'start_date_parameter': fields.String,
        'end_date_parameter': fields.String,
        'duration': db.Integer,
        'status': db.Boolean
    }

    def __init__(self, creator_id, category = None, event_name = None, place_name = None, place_location = None, start_date = None, end_date = None, start_date_parameter, end_date_parameter, duration, status):
        self.creator_id = creator_id
        self.category = category
        self.event_name = event_name
        self.place_name = place_name
        self.place_location = place_location
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_parameter = start_date_parameter
        self.end_date_parameter = end_date_parameter
        self.duration = duration
        self.status = status

    def __repr__(self):
        return '<Events %r>' % self.event_id