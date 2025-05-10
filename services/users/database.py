from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexão para o banco de dados de usuários
DATABASE_URL = "postgresql+psycopg2://ecommerce_users:my_password_users@ecommerce-db-users:5432/ecommerce_users"

# Cria o engine de conexão
engine = create_engine(DATABASE_URL)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
