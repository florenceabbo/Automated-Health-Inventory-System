from backend.db import db
from dataclasses import dataclass

@dataclass
class DispensedStock(db.Model):
  __tablename__ = 'dispensed_stocks'
  id:int
  status:str
  medical_supply_id:int
  medical_supply_quantity= str
  medicine_id:int
  medicine_quantity= str
  

  id = db.Column(db.Integer, primary_key = True)
  status = db.Column(db.String(100))
  medical_supply_id = db.Column(db.Integer,db.ForeignKey('medical_supplies.id'))
  medical_supply_quantity=db.Column(db.String(250))
  medicine_id= db.Column(db.Integer,db.ForeignKey('medicines.id'))
  medicine_quantity=db.Column(db.String(250))
  created_by  = db.Column(db.Integer,db.ForeignKey('users.id'))
  created_at = db.Column(db.String(255),nullable=True)
  updated_at = db.Column(db.String(255),nullable=True)
  


  def __init__(self,status,medical_supply_id,medical_supply_quantity,medicine_id, medicine_quantity,created_by,created_at,updated_at):
   self.status = status
  
   self.medicine_id = medicine_id 
   self. medicine_quantity=  medicine_quantity
   self.medical_supply_id = medical_supply_id
   self.medical_supply_quantity =medical_supply_quantity
   self.created_by = created_by
   self.created_at = created_at
   self.updated_at =updated_at

  

def __repr__(self):
  return f"<DispensedStock {self.name} >"
  

        
   #save a new instance
def save(self):
    db.session.add(self)
    db.session.commit()

   #delete the item
def delete(self):
    db.session.delete(self)
    db.session.commit()