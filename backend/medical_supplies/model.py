from backend.db import db
from dataclasses import dataclass

@dataclass
class MedicalSupply(db.Model):
  __tablename__ = 'medical_supplies'
  id:int
  name:str
  price_unit:str
  image:str
  stock:int
  medical_supply_category_id:int

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100),unique=True)
  price_unit = db.Column(db.String(10),default='UGX')
  image = db.Column(db.String(200))
  stock = db.Column(db.Integer)
  medical_supply_category_id = db.Column(db.Integer,db.ForeignKey('medical_supply_categories.id'))
  created_by  = db.Column(db.Integer,db.ForeignKey('users.id'))
  created_at = db.Column(db.String(255),nullable=True)
  updated_at = db.Column(db.String(255),nullable=True)
  


  def __init__(self, name,image,price_unit,stock,medical_supply_category_id,created_by,created_at,updated_at):
   self.name = name
   self.image = image
   self.price_unit = price_unit 
   self.medical_supply_category_id = medical_supply_category_id
   self.stock = stock
   self.created_by = created_by
   self.created_at = created_at
   self.updated_at =updated_at

  

def __repr__(self):
  return f"<MedicalSupply {self.name} >"
  

        
   #save a new instance
def save(self):
    db.session.add(self)
    db.session.commit()

   #delete the item
def delete(self):
    db.session.delete(self)
    db.session.commit()