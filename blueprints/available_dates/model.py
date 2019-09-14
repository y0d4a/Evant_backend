from blueprints import db
from flask_restful import fields

class AvailableDates(db.Model):
    """class for available_dates"""

    __tablename__= "dates"

    user_id = db.Column(db.Integer, nullable = False, primary_key=True)
    date = db.Column(db.String(25), nullable= False, primary_key=True)

    response_fields = {
        'user_id'  : fields.Integer,
        'date'  : fields.String
    }

    def __init__(self,user_id, date):
        self.user_id = user_id
        self.date = date