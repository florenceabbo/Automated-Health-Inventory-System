import os
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS =False


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    JWT_SECRET_KEY = "super-secret"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/Automated_Health_Inventory_system'

class TestingConfig(Config):
    DEBUG = True
    TESTING =True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")


Config= {
   'development':DevelopmentConfig,
   'testing':TestingConfig,
   'default':DevelopmentConfig 
}