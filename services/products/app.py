from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List  # Aqui está a correção
from services.products.database import SessionLocal, engine
from services.products.models import Base, Product
from pydantic import BaseModel

app = FastAPI()

# Garante que as tabelas sejam criadas no banco
Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquemas Pydantic para entrada e resposta de dados
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

class ProductUpdate(BaseModel):
    name: str
    price: float
    quantity: int

class ProductResponse(BaseModel):  # Novo modelo de resposta
    product_id: int
    name: str
    price: float
    quantity: int

    class Config:
        orm_mode = True

@app.post("/products", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(name=data.name, price=data.price, quantity=data.quantity)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products", response_model=List[ProductResponse])  # Corrigido com List importado
def list_products(db: Session = Depends(get_db)):
    stmt = select(Product)
    products = db.execute(stmt).scalars().all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return ProductResponse(product_id=product.id, name=product.name, price=product.price, quantity=product.quantity)

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    product.name = data.name
    product.price = data.price
    product.quantity = data.quantity
    db.commit()
    db.refresh(product)
    return ProductResponse(product_id=product.id, name=product.name, price=product.price, quantity=product.quantity)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(product)
    db.commit()
    return {"message": "Produto deletado com sucesso"}


