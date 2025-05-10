from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from services.orders.database import SessionLocal, engine
from services.orders.models import Base, Order
from pydantic import BaseModel
from typing import List

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class OrderCreate(BaseModel):
    user_id: int
    products: List[int]  # IDs dos produtos

class OrderUpdate(BaseModel):
    user_id: int
    products: List[int]

class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    products: List[int]

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(user_id=order.user_id, products=order.products)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    stmt = select(Order)
    return db.execute(stmt).scalars().all()

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return db_order

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db_order.user_id = order_update.user_id
    db_order.products = order_update.products
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(db_order)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}
