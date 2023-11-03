from backend.db import db
from dataclasses import dataclass

@dataclass
class StockOrder(db.Model):
  __tablename__ = 'stock_orders'
  id:int
  status:str
  quantity:str
  medical_supply_id:int
  medicine_id:int

  id = db.Column(db.Integer, primary_key = True)
  status = db.Column(db.String(100),unique=True)
  quantity = db.Column(db.String(250), unique=True)
  medical_supply_id = db.Column(db.Integer,db.ForeignKey('medical_supplies.id'))
  medicine_id= db.Column(db.Integer,db.ForeignKey('medicines.id'))
  created_by  = db.Column(db.Integer,db.ForeignKey('users.id'))
  created_at = db.Column(db.String(255),nullable=True)
  updated_at = db.Column(db.String(255),nullable=True)
  


  def __init__(self,status,quantity,medical_supply_id,medicine_id,created_by,created_at,updated_at):
   self.status = status
   self.quantity = quantity
   self.medicine_id = medicine_id 
   self.medical_supply_id = medical_supply_id
   self.created_by = created_by
   self.created_at = created_at
   self.updated_at =updated_at

  

def __repr__(self):
  return f"<StockOrder {self.name} >"
  

        
   #save a new instance
def save(self):
    db.session.add(self)
    db.session.commit()

   #delete the item
def delete(self):
    db.session.delete(self)
    db.session.commit()