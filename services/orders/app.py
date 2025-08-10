from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import List

from services.orders.database import SessionLocal, engine
from services.orders.models import Base, Order

app = FastAPI()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Novo esquema para produtos com quantidade
class ProductQuantity(BaseModel):
    product_id: int
    quantity: int

# Schemas para entrada e saída
class OrderCreate(BaseModel):
    user_id: int
    products: List[ProductQuantity]

class OrderUpdate(BaseModel):
    user_id: int
    products: List[ProductQuantity]

class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    products: List[ProductQuantity]

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Converte produtos para lista de dicts para o JSON
    products_json = [p.dict() for p in order.products]
    db_order = Order(user_id=order.user_id, products=products_json)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return {"order_id": db_order.id, "user_id": db_order.user_id, "products": db_order.products}

import traceback
from fastapi.responses import JSONResponse

@app.get("/orders", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    try:
        orders = db.execute(select(Order)).scalars().all()
        return [
            {"order_id": o.id, "user_id": o.user_id, "products": o.products}
            for o in orders
        ]
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"order_id": db_order.id, "user_id": db_order.user_id, "products": db_order.products}

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db_order.user_id = order_update.user_id
    db_order.products = [p.dict() for p in order_update.products]
    db.commit()
    db.refresh(db_order)
    return {"order_id": db_order.id, "user_id": db_order.user_id, "products": db_order.products}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db.delete(db_order)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}
