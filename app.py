from backend import create_app,db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
 
from backend.users.model import User
from backend.medical_supplies.model import MedicalSupply
from backend.medical_supply_categories.model import MedicalSupplyCategory
from backend.medicines.model import Medicine 
from backend.medicine_categories. model import MedicineCategory
from backend.stock_orders.model import StockOrder
from backend.received_purchases.model import ReceivedPurchase
from backend.dispensed_stocks.model import DispensedStock
 






app = create_app('development')
migrate = Migrate(app,db)
jwt=JWTManager(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,MedicalSupply=MedicalSupply, 
                 MedicalSupplyCategory=MedicalSupplyCategory, 
                 User=User,Medicine=Medicine,
                 MedicineCategory= MedicineCategory, 
                 StockOrder=StockOrder, 
                 ReceivedPurchase=ReceivedPurchase,
                 DispensedStock=DispensedStock)  
