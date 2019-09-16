from blueprints import db
from flask_restful import fields

class UserPreferences(db.Model):
    __tablename__="user_preferences"

    user_id = db.Column(db.Integer, nullable = False, primary_key=True)
    event_id = db.Column(db.Integer, nullable = False, primary_key=True)
    preference = db.Column(db.String(50), nullable= False)
    confirmation = db.Column(db.Integer, nullable=False)

    response_fields = {
        'user_id' : fields.Integer,
        'event_id' : fields.Integer,
        'preference' : fields.String,
        'confirmation':fields.Integer
    }

    def __init__(self,user_id, event_id, preference, confirmation=0):
        self.user_id = user_id
        self.event_id = event_id
        self.preference = preference
        self.confirmation = confirmation