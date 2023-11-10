# Register a new stock order
from flask import jsonify, request, Blueprint
from backend.received_purchases.model import ReceivedPurchase
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for stock orders, where stock orders is the resource
received_purchases = Blueprint('received_purchases',__name__,url_prefix='/received_purchases')

#Getting all orders
@received_purchases.route("/")
def get_all_received_purchases():
    received_purchases = ReceivedPurchase.query.all()
    return jsonify({
            "success":True,
            "data":received_purchases,
            "total":len(received_purchases)
        }),200

#creating districts


@received_purchases.route('/create', methods= ['POST'])
@jwt_required()
def create_new_medicine():

    data = request.get_json()
    status = data['status']
    medical_supply_quantity = data['medical_supply_quantity']
    medicine_quantity= data['medicine_quantity']
    stock_order_id = data['stock_order_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not status:
        return jsonify({'error':"Stock purchase status is required"})
   
    
    if not medical_supply_quantity:
        return jsonify({'error':"The specofic received stock medical_supply_quantity is required"})
    if not  medicine_quantity:
        return jsonify({'error':"The specific received stock medicine is required"})

    if not  stock_order_id:
        return jsonify({'error':"The specific order id is required"})
    


    if ReceivedPurchase.query.filter_by(created_by=created_by).first() is not None and ReceivedPurchase.query.filter_by(stock_order_id=stock_order_id).first():
        return jsonify({'error': "This order has already been recieved"}), 409 

    new_received_purchase = ReceivedPurchase(medical_supply_quantity= medical_supply_quantity,medicine_quantity=medicine_quantity,created_by=created_by,stock_order_id=stock_order_id,status=status,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(new_received_purchase)
    db.session.commit()
    return jsonify({'message':'New order created sucessfully','data': [new_received_purchase.id,new_received_purchase.medical_supply_quantity,new_received_purchase.medicine_quantity,new_received_purchase.status,new_received_purchase.stock_order_id,new_received_purchase.created_by,new_received_purchase.created_at,new_received_purchase.updated_at]}),201

@received_purchases.route('/order/<id>', methods=['GET'])
def get_received_purchase(id):
    received_purchase_id= ReceivedPurchase.query.get(id)
    results = {
        "medical_supply_quantity": received_purchase_id.medical_supply_quantity,
        "medicine_quantity": received_purchase_id.medicine_quantity,
        "status":received_purchase_id.status,
        "stock_order_id":received_purchase_id.stock_order_id,
        "created_by":received_purchase_id.created_by,
        "created_at":received_purchase_id.created_at
        
    }
         
    return jsonify({"Success": True, "ReceivedPurchase": results,"Message":"Received purchase details retrieved"})

          
    # put
@received_purchases.route('/update/<int:id>', methods=['PUT'])
def update_received_purchase(id):
    received_purchase = ReceivedPurchase.query.get_or_404(id)
    received_purchase.medical_supply_quantity = request.json['medical_supply_quantity']
    received_purchase.medicine_quantity =request.json['medicine_quantity']
    received_purchase.status =request.json['status']
    received_purchase.stock_order_id =request.json['stock_order_id']
    received_purchase.updated_at=datetime.utcnow() 

    db.session.add(received_purchase)
    db.session.commit()
    return jsonify({"message":"Received purchase details updated successfully"})


# delete
@received_purchases.route('/delete/<id>', methods=['DELETE'])
def delete_received_purchase(id):
    delete_id = ReceivedPurchase.query.get(id)

    if delete_id is None:
        return{"Message":"This Received purchase doesnot exist"}
    # Order doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Received purchase deleted successfully."})
        
   
  
   
  
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