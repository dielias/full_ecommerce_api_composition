from sqlalchemy import Column, Integer, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # ID do usuário que fez o pedido
    products = Column(ARRAY(Integer), nullable=False)  # IDs dos produtos no pedido (sem chave estrangeira)

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, products={self.products})>"



