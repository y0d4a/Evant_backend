from blueprints import db
from flask_restful import fields

class Categories (db.Model):
    """class for category"""

    __tablename__= "categories"

    preference = db.Column(db.String(100), nullable = False, primary_key=True)
    category = db.Column(db.String(100), nullable= False)

    response_fields = {
        'preferences'  : fields.String,
        'category'  : fields.String
    }

    def __init__(self, preference, category):
        self.preference = preference
        self.category = category