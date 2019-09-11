from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS
import config, os

app = Flask(__name__)
app.config['APP_DEBUG'] = True
CORS(app)

######################
# CHOOSING DATABASE
######################
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

except Exception as e:
    raise e

#####################
# JWT
#####################
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)


######################
# DATABASE
######################
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta123@localhost:3306/eCommerce'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Altabatch3@databasesyamsulclub.cdbtzlgoj2dv.ap-southeast-1.rds.amazonaws.com:3306/eCommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#############
# RESOURCES
#############
