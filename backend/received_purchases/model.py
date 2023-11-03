from backend.db import db
from dataclasses import dataclass

@dataclass
class ReceivedPurchase(db.Model):
  __tablename__ = 'received_purchases'
  id:int
  status:str
  quantity:str
  stock_order_id:int

  id = db.Column(db.Integer, primary_key = True)
  status = db.Column(db.String(100),unique=True)
  quantity = db.Column(db.String(250), unique=True)
  stock_order_id= db.Column(db.Integer,db.ForeignKey('stock_orders.id'))
  created_by  = db.Column(db.Integer,db.ForeignKey('users.id'))
  created_at = db.Column(db.String(255),nullable=True)
  updated_at = db.Column(db.String(255),nullable=True)
  


  def __init__(self,status,quantity,stock_order_id,created_by,created_at,updated_at):
   self.status = status
   self.quantity = quantity
   self.stock_order_id = stock_order_id 
   self.created_by = created_by
   self.created_at = created_at
   self.updated_at =updated_at

  

def __repr__(self):
  return f"<ReceivedPurchase {self.name} >"
  

        
   #save a new instance
def save(self):
    db.session.add(self)
    db.session.commit()

   #delete the item
def delete(self):
    db.session.delete(self)
    db.session.commit()