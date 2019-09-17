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
        app.config.from_object(config.SyamsulLocalConfig)
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
from blueprints.user_preferences.resource import bp_user_preferences
from blueprints.users.resource import bp_user
from blueprints.invitations.resource import bp_invitations
from blueprints.available_dates.resource import bp_available_dates
from blueprints.categories.resource import bp_categories
from blueprints.events.resource import bp_events
from blueprints.third_party import bp_third_party


app.register_blueprint(bp_invitations, url_prefix='/api/invitations')
app.register_blueprint(bp_available_dates, url_prefix='/api/date')
app.register_blueprint(bp_user, url_prefix='/api/users')
app.register_blueprint(bp_user_preferences, url_prefix='/api/users/preferences')
app.register_blueprint(bp_categories, url_prefix='/api/category')
app.register_blueprint(bp_events, url_prefix='/api/events')
app.register_blueprint(bp_third_party, url_prefix='/api/recommendation')



db.create_all()