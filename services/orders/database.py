from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://ecommerce_orders:my_password_orders@ecommerce-db-orders:5432/ecommerce_orders"

# Cria a engine de conexão com o banco de dados do serviço de pedidos
engine = create_engine(DATABASE_URL)

# Cria uma sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
