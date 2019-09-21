class Config():
    pass

class DevelopmentConfig(Config):
    '''development'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:evantadmin@cobaevant.cwpvjetmrbmv.ap-southeast-1.rds.amazonaws.com:3306/evant'

class TestingConfig(Config):
    '''testing'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:evantadmin@cobaevant.cwpvjetmrbmv.ap-southeast-1.rds.amazonaws.com:3306/evant_test'

