from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexão exclusiva do serviço de produtos
DATABASE_URL = "postgresql+psycopg2://ecommerce_products:my_password_products@toxiproxy-products:25432/ecommerce_products"

# Criação da engine
engine = create_engine(DATABASE_URL)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)