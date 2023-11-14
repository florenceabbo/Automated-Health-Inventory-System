# Register a new dispensed stock 
from flask import jsonify, request, Blueprint
from backend.dispensed_stocks.model import DispensedStock
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 
 


# Creating a blue print for dispensed stock, where dispensed stock is the resource
dispensed_stocks = Blueprint('dispensed_stocks',__name__,url_prefix='/dispensed_stocks')

#Getting all orders
@dispensed_stocks.route("/")
def get_all_dispensed_stocks():
    dispensed_stocks = DispensedStock.query.all()
    return jsonify({
            "success":True,
            "data":dispensed_stocks,
            "total":len(dispensed_stocks)
        }),200

#creating districts


@dispensed_stocks.route('/create', methods= ['POST'])
@jwt_required()
def create_new_medicine():

    data = request.get_json()
    status = data['status']
    medical_supply_id = data['medical_supply_id']
    medical_supply_quantity= data['medical_supply_quantity']
    medicine_id = data['medicine_id']
    medicine_quantity= data['medicine_quantity']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not status:
      return jsonify({'error':"Dispensed_stock status is required"})
   

    if not  medical_supply_id:
       return jsonify({'error':"Medical_supply_id being dispensed is required"})
    if not medical_supply_quantity:
      return jsonify({'error': "medical_supply_quantity being dispensed is required"})
    
    if not medicine_id:
      return jsonify({'error':"The medicine_id being dispensed  is required"})
    if not medicine_quantity:
      return jsonify({'error': "The medicine_quantity being dispensed is required"})


    if DispensedStock.query.filter_by(created_by=created_by).first() is not None and DispensedStock.query.filter_by(medical_supply_id=medical_supply_id).first() is not None and DispensedStock.query.filter_by(medicine_id=medicine_id).first():
      return jsonify({'error': "This dispensery stock has already been created"}), 409 

    new_dispensed_stock = DispensedStock(status=status,medical_supply_id=medical_supply_id,medical_supply_quantity=medical_supply_quantity,medicine_id=medicine_id,medicine_quantity=medicine_quantity,created_by=created_by,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(new_dispensed_stock)
    db.session.commit()
    return jsonify({'message':'New dispensed stock created sucessfully','data': [new_dispensed_stock.id,new_dispensed_stock.medical_supply_quantity, new_dispensed_stock.medicine_quantity,new_dispensed_stock.status,new_dispensed_stock.created_by,new_dispensed_stock.created_at,new_dispensed_stock.updated_at,new_dispensed_stock.medical_supply_id,new_dispensed_stock.medicine_id]}),201

@dispensed_stocks.route('/order/<id>', methods=['GET'])
def get_dispensed_stock(id):
    dispensed_stock_id= DispensedStock.query.get(id)
    results = {
        
        "status":dispensed_stock_id.status,
        "medical_supply_id":dispensed_stock_id.medical_supply_id,
        "medicical_supply_quantity": dispensed_stock_id.medical_supply_quantity,
        "medicine_id":dispensed_stock_id.medicine_id,
        "medicine_quantity": dispensed_stock_id.medicine_quantity,
        "created_by":dispensed_stock_id.created_by,
        "created_at":dispensed_stock_id.created_at
        
    }
         
    return jsonify({"Success": True, "DispensedStock": results,"Message":" Dispensed Stock details retrieved"})

          
    # put
@dispensed_stocks.route('/update/<int:id>', methods=['PUT'])
def update_dispensed_stock(id):
    dispensed_stock = DispensedStock.query.get_or_404(id)

   
    dispensed_stock.status =request.json['status']
    dispensed_stock.medical_supply_id =request.json['medical_supply_id']
    dispensed_stock.medical_supply_quantity = request.json['medical_supply_quantity']
    dispensed_stock.medicine_id =request.json['medicine_id']
    dispensed_stock.medicine_quantity =request.json['medicine_quantity']
    dispensed_stock.updated_at=datetime.utcnow() 

    db.session.add(dispensed_stock)
    db.session.commit()
    return jsonify({"message":"Dispensed StocK details updated successfully"})


# delete
@dispensed_stocks.route('/delete/<id>', methods=['DELETE'])
def delete_dispensed_stock(id):
    delete_id = DispensedStock.query.get(id)

    if delete_id is None:
        return{"Message":"This Dispensed Stock doesnot exist"}
    # Order doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"This Dispensed Stock deleted successfully."})
        
   
  
   
  
# #   getting all medical supplies from the medical_ supply category
# @medical_supplies.route('/medical_supply_categories/<medical_supply_category>' , methods=['GET'])
# def items_under_a_subcategory(medical_supply_category):
#     response = MedicalSupply.query.filter_by(medical_supply_category_id=medical_supply_category)
#     returned_medical_supplies = [
#          {
#         'name':w.name,
#         'price_unit':w.price_unit,
#         'image':w.image,
#         'medical_supply_category':w.medical_supply_category
        
#         }
#         for w in response

#     ]
#     return {
#         'MedicalSupply':returned_medical_supplies
#     }