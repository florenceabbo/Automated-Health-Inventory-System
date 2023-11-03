# Register a new medicine
from flask import jsonify, request, Blueprint
from backend.medicines.model import Medicine
from backend.db import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required 


# Creating a blue print for medicines, where medicine is the resource
medicines = Blueprint('medicines',__name__,url_prefix='/medicines')

#Getting all orders
@medicines.route("/")
def get_all_medicines():
    medicines = Medicine.query.all()
    return jsonify({
            "success":True,
            "data":medicines,
            "total":len(medicines)
        }),200

#creating districts


@medicines.route('/create', methods= ['POST'])
@jwt_required()
def create_new_medicine():

    data = request.get_json()
    name = data['name']
    unit_price = data['unit_price']
    image = data['image']
    stock = data['stock']
    medicine_category_id= data['medicine_category_id']
    created_by =  get_jwt_identity()
      
  
    #validations
    if not name:
        return jsonify({'error':"Medicine name is required"})
   
    
    if not unit_price:
        return jsonify({'error':"The cost of Medicine perunit is required"})

    if not image:
        return jsonify({'error':" Medicine image is required"})
    
    if not stock:
        return jsonify({'error':"The quantity in stock  is required"})
    if not medicine_category_id:
        return jsonify({'error':" The medicine category name  is required"})
         
    

    if Medicine.query.filter_by(name=name).first() is not None and Medicine.query.filter_by(created_by=created_by).first():
        return jsonify({'error': "This Medicine  already exsists"}), 409 

    medicines = Medicine(name=name,created_by=created_by,unit_price=unit_price,image=image,stock=stock,medicine_category_id=medicine_category_id,created_at=datetime.now(),updated_at=datetime.now()) 
    #The datetime.now() function auto generates the current date  
    #inserting values
    db.session.add( medicines)
    db.session.commit()
    return jsonify({'message':'New Medical supply item created sucessfully','data': [medicines.id,medicines.name,medicines.created_by,medicines.created_at,medicines.updated_at,medicines.unit_price,medicines.image,medicines.stock, medicines.medicine_category_id]}),201

@medicines.route('/get/<id>', methods=['GET'])
def get_medicines(id):
    medicine_id= Medicine.query.get(id)
    results = {
        "id":medicine_id.id,
        "name": medicine_id.name,
        "unit_price":medicine_id.price_unit,
        "image":medicine_id.image,
        "stock":medicine_id.stock,
        "medicine_category_id":medicine_id.medicine_category_id,
        "created_by":medicine_id.created_by,
        "created_at":medicine_id.created_at
        
    }
    
    return jsonify({"Success": True, "Medicine": results,"Message":"Medicine item details retrieved"})

          
    # put
@medicines.route('/update/<id>', methods=['PUT'])
def update_medicalsupply(id):
    medicine = Medicine.query.get_or_404(id)

    medicine.name =request.json['name']
    medicine.unit_price =request.json['unit price']
    medicine.image =request.json['image']
    medicine.stock =request.json['stock']
    medicine.medicine_category_id =request.json['medicine_category_id']
    medicine.updated_at=datetime.utcnow() 

    db.session.add(medicine)
    db.session.commit()
    return jsonify({"message":"This Medicine was updated successfully"})


# delete
@medicines.route('/delete/<id>', methods=['DELETE'])
def delete_medicine(id):
    delete_id = medicines.query.get(id)

    if delete_id is None:
        return{"Message":" This Medicine doesnot exist"}
    # user doesnot exist
    db.session.delete(delete_id)
    db.session.commit()
    return jsonify({"message":"Medicine deleted successfully."})
        
   
  
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