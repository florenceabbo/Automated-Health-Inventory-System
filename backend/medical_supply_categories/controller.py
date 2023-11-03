# Register a new medical supplycategory
from flask import jsonify, request, Blueprint
from backend.medical_supply_categories.model import MedicalSupplyCategory
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for medical supply category, where medical supply category is the resource
medical_supply_categories = Blueprint('medical_supply_categories',__name__,url_prefix='/medical_supply_categories')

#Getting all medical_supply_categories
@medical_supply_categories.route("/")
def get_all_subfoodcategories():
    medical_supply_categories = MedicalSupplyCategory.query.all()
    return jsonify({
            "success":True,
            "data":medical_supply_categories,
            "total":len(medical_supply_categories)
        }),200

#creating medical_supply_category


@medical_supply_categories.route('/create', methods= ['POST'])
@jwt_required()
def create_new_medicalsupplycategory():

    data = request.get_json()
    name = data['name']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
         return jsonify({'error':"Sub food category name is required"})
   
    

    if MedicalSupplyCategory.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "This medical supply category name exists"}), 409 

    new_medical_supply_category = MedicalSupplyCategory(name=name,created_by=created_by,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add(new_medical_supply_category)
    db.session.commit()
    return jsonify({'message':'New Sub food category created sucessfully','data': [new_medical_supply_category.id,new_medical_supply_category.name,new_medical_supply_category.created_by,new_medical_supply_category.created_at,new_medical_supply_category.updated_at]}),201

@medical_supply_categories.route('/get/<id>', methods=['GET'])
def get_medicalsupplycategory(id):
    medical_supply_category_id= MedicalSupplyCategory.query.get(id)
    results = {
        "name": medical_supply_category_id.name,
        "created_by":medical_supply_category_id.created_by,
        "created_at":medical_supply_category_id.created_at
        
    }
         
    return jsonify({"Success": True, "MedicalSupplyCategory": results,"Message":"Medical supply category details retrieved"})

          
    # put
@medical_supply_categories.route('/update/<int:id>', methods=['PUT'])
def update_medicalsupplycategory(id):
    medical_supply_category = MedicalSupplyCategory.query.get_or_404(id)

    medical_supply_category.name =request.json['name']
    medical_supply_category.updated_at=datetime.utcnow() 

    db.session.add(medical_supply_category)
    db.session.commit()
    return jsonify({"message":"Medical supply category updated successfully"})


# delete
@medical_supply_categories.route('/delete/<id>', methods=['DELETE'])
def delete_medicalsupplycategory(id):
    delete_id = MedicalSupplyCategory.query.get(id)

    if delete_id is None:
        return{"Message":"This medical supply category doesnot exist"}
    # medical supply category doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Medicl supply category deleted successfully."})
