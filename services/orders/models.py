from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    products = Column(JSON, nullable=False)  # lista de dicts {product_id, quantity}

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, products={self.products})>"






