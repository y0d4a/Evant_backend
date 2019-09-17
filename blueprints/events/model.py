from blueprints import db
from flask_restful import fields

class Events(db.Model):

    """ Events Table Database """

    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key = True)
    creator_id = db.Column(db.Integer, nullable = False)
    category = db.Column(db.String(100), nullable = True)
    event_name = db.Column(db.String(100), nullable = False)
    start_date_parameter = db.Column(db.String(100), nullable = True)
    end_date_parameter = db.Column(db.String(100), nullable = True)
    duration = db.Column(db.Integer, nullable = True)
    status = db.Column(db.Integer, nullable = False)
    place_name = db.Column(db.String(250), nullable = True)
    place_location = db.Column(db.String(250), nullable = True)
    start_date = db.Column(db.String(100), nullable = True)
    end_date = db.Column(db.String(100), nullable = True)   
    preference = db.Column(db.String(100), nullable = True)
    creator_confirmation = db.Column(db.Integer, nullable=True)


    response_fields = {
        'event_id' : fields.Integer,
        'creator_id': fields.Integer,
        'category' : fields.String,
        'event_name': fields.String,
        'start_date_parameter': fields.String,
        'end_date_parameter': fields.String,
        'duration': fields.Integer,
        'status': fields.Integer,
        'place_name': fields.String,
        'place_location': fields.String,
        'start_date': fields.String,
        'end_date': fields.String,
        'preference': fields.String,
        'creator_confirmation':fields.Integer
    }

    def __init__(self, creator_id, category, event_name, start_date_parameter, end_date_parameter, duration, status, place_name = None, place_location = None, start_date = None, end_date = None, preference = None, creator_confirmation=1):
        self.creator_confirmation = creator_confirmation
        self.creator_id = creator_id
        self.category = category
        self.event_name = event_name
        self.start_date_parameter = start_date_parameter
        self.end_date_parameter = end_date_parameter
        self.duration = duration
        self.status = status
        self.place_name = place_name
        self.place_location = place_location
        self.start_date = start_date
        self.end_date = end_date
        self.preference = preference
        
