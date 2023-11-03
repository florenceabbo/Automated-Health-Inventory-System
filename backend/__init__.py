from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from backend.db import db
#from flask_jwt_extended import JWTManager
from flask_cors import CORS
#from flask_jwt_extended import get_jwt_identity



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config[config_name])
    Config[config_name].init_app(app)
    
    #app.config["JWT_ALGORITHM"] = "HS256"
    app.config.from_pyfile("../config.py")
    app.app_context()
    
  


    db.init_app(app)
    CORS(app)
    
   
    #importing blueprint
   
    from backend.users.controller import users
    from backend.medical_supplies.controller import medical_supplies
    from backend.medical_supply_categories.controller import medical_supply_categories
    from backend.medicines.controller import medicines
    from backend.stock_orders.controller import stock_orders
    from backend.received_purchases.controller import received_purchases
    from backend.medicine_categories.contoller import medicine_categories
   
   
    
   
      #registering blueprint for the route to work
      #app.register_blueprint(users) takes in the blueprint instance as the paramenter.
    
    app.register_blueprint(users)
    app.register_blueprint(medical_supplies)
    app.register_blueprint(medical_supply_categories)
    app.register_blueprint(medicines)
    app.register_blueprint(stock_orders) 
    app.register_blueprint(received_purchases)
    app.register_blueprint(medicine_categories)
   
  


    return app