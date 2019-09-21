from blueprints import db
from flask_restful import fields

class Users(db.Model):

    """ Users Table Database """

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = True)
    gender = db.Column(db.Boolean, nullable = True)
    status_first_login = db.Column(db.Boolean, nullable = True)
    fullname = db.Column(db.String(100), nullable = True)
    address = db.Column(db.String(100), nullable = True)
    phone = db.Column(db.String(30), nullable = True)
    token_broadcast = db.Column(db.String(400), nullable = True)

    response_fields = {
        'user_id' : fields.Integer,
        'username' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'gender' : fields.Boolean,
        'status_first_login' : fields.Boolean,
        'fullname' : fields.String,
        'address' : fields.String,
        'phone' : fields.String,
        'token_broadcast' : fields.String,     
    }

    jwt_response_fields = {
        'user_id' : fields.Integer,
        'username' : fields.String,
        'email' : fields.String,
        'gender' : fields.Boolean,
        'status_first_login' : fields.Boolean,
        'fullname' : fields.String,
        'address' : fields.String,
        'phone' : fields.String,
        'token_broadcast' : fields.String,
    }

    def __init__(self, username, email, password=None, gender=None, status_first_login=None, fullname = None, address = None, phone = None, token_broadcast = None):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.status_first_login = status_first_login
        self.fullname = fullname
        self.address = address
        self.phone = phone
        self.token_broadcast = token_broadcast
    
    def __repr__(self):
        return '<Users %r>' % self.user_id
        
