# Register a new medicine category
from flask import jsonify, request, Blueprint
from backend.medicine_categories.model import MedicineCategory
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for orders, where orders is the resource
medicine_categories = Blueprint('medicine_categories',__name__,url_prefix='/medicine_categories')

#Getting all orders
@medicine_categories.route("/")
def get_all_medicine_categories():
    medicine_categories = MedicineCategory.query.all()
    return jsonify({
            "success":True,
            "data":medicine_categories,
            "total":len(medicine_categories)
        }),200

#creating districts


@medicine_categories.route('/create', methods= ['POST'])
@jwt_required()
def create_new_medicinecategory():

    data = request.get_json()
    name = data['name']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
        return jsonify({'error':"Medicine category name is required"})
   
         
    

    if MedicineCategory.query.filter_by(name=name).first() is not None and MedicineCategory.query.filter_by(created_by=created_by).first():
        return jsonify({'error': "This Medicine  already exsists"}), 409 

    medicine_categories = MedicineCategory(name=name,created_by=created_by,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(medicine_categories)
    db.session.commit()
    return jsonify({'message':'New Medical supply item created sucessfully','data': [medicine_categories.id,medicine_categories.name,medicine_categories.created_by,medicine_categories.created_at,medicine_categories.updated_at]}),201

@medicine_categories.route('/get/<id>', methods=['GET'])
def get_medicalsupply(id):
    medicine_category_id= MedicineCategory.query.get(id)
    results = {
        "id":medicine_category_id.id,
        "name": medicine_category_id.name,
        "created_by":medicine_category_id.created_by,
        "created_at":medicine_category_id.created_at
        
    }
    
    return jsonify({"Success": True, "MedicineCategory": results,"Message":"Medicine Category item details retrieved"})

          
    # put
@medicine_categories.route('/update/<id>', methods=['PUT'])
def update_medicine_category(id):
    medicine = MedicineCategory.query.get_or_404(id)

    medicine.name =request.json['name']
    medicine.updated_at=datetime.utcnow() 

    db.session.add(medicine)
    db.session.commit()
    return jsonify({"message":"This Medicine Category was updated successfully"})


# delete
@medicine_categories.route('/delete/<id>', methods=['DELETE'])
def delete_medicine_category(id):
    delete_id = medicine_categories.query.get(id)

    if delete_id is None:
        return{"Message":" This Medicine Category doesnot exist"}
    # user doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Medicine Category deleted successfully."})
        
   
  
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