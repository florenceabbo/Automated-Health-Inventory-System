# Register a new stock order
from flask import jsonify, request, Blueprint
from backend.stock_orders.model import StockOrder
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for stock orders, where stock orders is the resource
stock_orders = Blueprint('stock_orders',__name__,url_prefix='/stock_orders')

#Getting all orders
@stock_orders.route("/")
def get_all_stock_orders():
    stock_orders = StockOrder.query.all()
    return jsonify({
            "success":True,
            "data":stock_orders,
            "total":len(stock_orders)
        }),200

#creating districts


@stock_orders.route('/create', methods= ['POST'])
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
        return jsonify({'error':"Stock order status is required"})
   

    if not  medical_supply_id:
        return jsonify({'error':"Medical_supply_id being ordered is required"})
    if not medical_supply_quantity:
        return jsonify({'error': "medical_supply_quantity being ordered is required"})
    
    if not medicine_id:
        return jsonify({'error':"The medicine_id being ordered  is required"})
    if not medicine_quantity:
        return jsonify({'error': "The medicine_quantity being ordered is required"})


    if StockOrder.query.filter_by(created_by=created_by).first() is not None and StockOrder.query.filter_by(medical_supply_id=medical_supply_id).first() is not None and StockOrder.query.filter_by(medical_supply_id=medical_supply_id).first():
        return jsonify({'error': "This order has already been made"}), 409 

    new_stock_order = StockOrder(medical_supply_quantity=medical_supply_quantity,created_by=created_by,medical_supply_id=medical_supply_id,medicine_id=medicine_id,medicine_quantity=medicine_quantity,status=status,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(new_stock_order)
    db.session.commit()
    return jsonify({'message':'New order created sucessfully','data': [new_stock_order.id,new_stock_order.medical_supply_quantity, new_stock_order.medicine_quantity,new_stock_order.status,new_stock_order.created_by,new_stock_order.created_at,new_stock_order.updated_at,new_stock_order.medical_supply_id,new_stock_order.medicine_id]}),201

@stock_orders.route('/order/<id>', methods=['GET'])
def get_stock_orders(id):
    stock_order_id= StockOrder.query.get(id)
    results = {
        "quantity": stock_order_id.quantity,
        "status":stock_order_id.status,
        "medical_supply_id":stock_order_id.medical_supply_id,
        "medicical_supply_quantity": stock_order_id.medical_supply_quantity,
        "medicine_id":stock_order_id.medicine_id,
        "medicine_quantity": stock_order_id.medicine_quantity,
        "created_by":stock_order_id.created_by,
        "created_at":stock_order_id.created_at
        
    }
         
    return jsonify({"Success": True, "StockOrder": results,"Message":"Stock order details retrieved"})

          
    # put
@stock_orders.route('/update/<int:id>', methods=['PUT'])
def update_stock_order(id):
    stock_order = StockOrder.query.get_or_404(id)

   
    stock_order.status =request.json['status']
    stock_order.medical_supply_id =request.json['medical_supply_id']
    stock_order.medical_supply_quantity = request.json['medical_supply_quantity']
    stock_order.medicine_id =request.json['medicine_id']
    stock_order.medicine_quantity =request.json['medicine_quantity']
    stock_order.updated_at=datetime.utcnow() 

    db.session.add(stock_order)
    db.session.commit()
    return jsonify({"message":"Stock Order details updated successfully"})


# delete
@stock_orders.route('/delete/<id>', methods=['DELETE'])
def delete_stock_order(id):
    delete_id = StockOrder.query.get(id)

    if delete_id is None:
        return{"Message":"This Stock Order doesnot exist"}
    # Order doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"This Stock Order deleted successfully."})
        
   
  
   
  
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