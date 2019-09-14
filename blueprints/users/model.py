from blueprints import db
from flask_restful import fields

class Users(db.Model):

    """ Users Table Database """

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    gender = db.Column(db.Boolean, nullable = False)
    status_first_login = db.Column(db.Boolean, nullable = False)
    fullname = db.Column(db.String(100), nullable = True)
    address = db.Column(db.String(100), nullable = True)
    phone = db.Column(db.String(30), nullable = True, unique = True)

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
    }

    def __init__(self, username, email, password, gender, status_first_login, fullname = None, address = None, phone = None):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.status_first_login = status_first_login
        self.fullname = fullname
        self.address = address
        self.phone = phone
    
    def __repr__(self):
        return '<Users %r>' % self.user_id
        
