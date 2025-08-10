from services.orders.database import SessionLocal, engine
from services.orders.models import Base, Order

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Deleta todos os registros existentes na tabela orders
db.query(Order).delete()
db.commit()

print("Todos os pedidos foram deletados com sucesso.")

db.close()
