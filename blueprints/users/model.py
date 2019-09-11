from blueprints import db
from flask_restful import fields

class Users(db.Model):

    """ Users Table Database """

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    gender = db.Column(db.Boolean, nullable = False)
    fullname = db.Column(db.String(255), nullable = True)
    address = db.Column(db.String(255), nullable = True)
    phone = db.Column(db.String(30), nullable = True, unique = True)

    response_fields = {
        'user_id' : fields.Integer,
        'username' : fields.String,
        'fullname' : fields.String,
        'address' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'phone' : fields.String,
        'gender' : fields.Integer,
    }

    jwt_response_fields = {
        'user_id' : fields.Integer,
        'username' : fields.String,
        'fullname' : fields.String,
        'address' : fields.String,
        'email' : fields.String,
        'phone' : fields.String,
        'gender' : fields.Integer,
    }

    def __init__(self, username, email, password, gender, fullname = None, address = None, phone = None):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.fullname = fullname
        self.address = address
        self.phone = phone
    
    def __repr__(self):
        return '<Users %r>' % self.user_id
        
