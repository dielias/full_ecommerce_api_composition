from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
import logging
import traceback
from fastapi.responses import JSONResponse

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

@app.get("/orders", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    try:
        orders = db.execute(select(Order)).scalars().all()
        response_data = []
        for o in orders:
            products_data = []
            for p in o.products:
                if isinstance(p, dict):
                    products_data.append(p)
                else:
                    logging.error(f"Formato inválido em pedido {o.id}: {o.products}")
            response_data.append({
                "order_id": o.id,
                "user_id": o.user_id,
                "products": products_data
            })
        return response_data
    except Exception as e:
        logging.exception("Erro ao listar pedidos")
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
