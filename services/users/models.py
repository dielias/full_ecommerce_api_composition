# services/users/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    # Relacionamento bidirecional com o modelo Order
    #orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")  # Relaciona com pedidos

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


