# Register a new medical supply
from flask import jsonify, request, Blueprint
from backend.medical_supplies.model import MedicalSupply
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for orders, where orders is the resource
medical_supplies = Blueprint('medical_supplies',__name__,url_prefix='/medical_supplies')

#Getting all orders
@medical_supplies.route("/")
def get_all_medicalsupplies():
    medical_supplies = MedicalSupply.query.all()
    return jsonify({
            "success":True,
            "data":medical_supplies,
            "total":len(medical_supplies)
        }),200

#creating districts


@medical_supplies.route('/create', methods= ['POST'])
@jwt_required()
def create_new_medical_supplly():

    data = request.get_json()
    name = data['name']
    unit_price = data['unit_price']
    image = data['image']
    stock = data['stock']
    medical_supply_category_id = data['medical_supply_category_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
        return jsonify({'error':"Medical supply item name is required"})
   
    
    if not unit_price:
        return jsonify({'error':"The cost of Medical supply item perunit is required"})

    if not image:
        return jsonify({'error':" Medical supply item image is required"})
    
    if not stock:
        return jsonify({'error':"The amount Medical supply item in stock  is required"})
    if not medical_supply_category_id:
        return jsonify({'error':" Sub Medical supply category name  is required"})
         
    

    if MedicalSupply.query.filter_by(name=name).first() is not None and MedicalSupply.query.filter_by(created_by=created_by).first():
        return jsonify({'error': "This Medical supply item  already exsists"}), 409 

    medical_supply = MedicalSupply(name=name,created_by=created_by,unit_price=unit_price,image=image,stock=stock,medical_supply_category_id=medical_supply_category_id,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add( medical_supply)
    db.session.commit()
    return jsonify({'message':'New Medical supply item created sucessfully','data': [medical_supply.id,medical_supply.name,medical_supply.created_by,medical_supply.price,medical_supply.created_at,medical_supply.updated_at,medical_supply.price_unit,medical_supply.image,medical_supply.stock, medical_supply.medical_supply_category_id]}),201

@medical_supplies.route('/get/<id>', methods=['GET'])
def get_medicalsupply(id):
    medical_supply_id= MedicalSupply.query.get(id)
    results = {
        "id":medical_supply_id.id,
        "name": medical_supply_id.name,
        "unit_price":medical_supply_id.unit_price,
        "image":medical_supply_id.image,
        "stock":medical_supply_id.stock,
        "medical_supply_category_id":medical_supply_id.medical_supply_category_id,
        "created_by":medical_supply_id.created_by,
        "created_at":medical_supply_id.created_at
        
    }
    
    return jsonify({"Success": True, "MedicalSupply": results,"Message":"Medical supply item details retrieved"})

          
    # put
@medical_supplies.route('/update/<id>', methods=['PUT'])
def update_medicalsupply(id):
    medical_supply = MedicalSupply.query.get_or_404(id)

    medical_supply.name =request.json['name']
    medical_supply.unit_price =request.json['unit_price']
    medical_supply.image =request.json['image']
    medical_supply.stock =request.json['stock']
    medical_supply.medical_supply_category_id =request.json['medical_supply_category_id']
    medical_supply.updated_at=datetime.utcnow() 

    db.session.add(medical_supply)
    db.session.commit()
    return jsonify({"message":"This Medical supply item updated successfully"})


# delete
@medical_supplies.route('/delete/<id>', methods=['DELETE'])
def delete_medicalsupply(id):
    delete_id = MedicalSupply.query.get(id)

    if delete_id is None:
        return{"Message":" This Medical supply item doesnot exist"}
    # user doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Medical supply item deleted successfully."})
        
   
  
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