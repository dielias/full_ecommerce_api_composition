import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from services.users.models import Base as BaseUsers, User
from services.products.models import Base as BaseProducts, Product
from services.orders.models import Base as BaseOrders, Order

# URLs de conexão para cada banco de dados
db_users_url = "postgresql+psycopg2://ecommerce_users:my_password_users@ecommerce-db-users:5432/ecommerce_users"
db_products_url = "postgresql+psycopg2://ecommerce_products:my_password_products@ecommerce-db-products:5432/ecommerce_products"
db_orders_url = "postgresql+psycopg2://ecommerce_orders:my_password_orders@ecommerce-db-orders:5432/ecommerce_orders"

# Criando as engines para cada banco de dados
engine_users = create_engine(db_users_url)
engine_products = create_engine(db_products_url)
engine_orders = create_engine(db_orders_url)

def wait_for_db(engine, db_name, retries=10, delay=5):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"✅ Banco '{db_name}' pronto para uso.")
            return
        except Exception as e:
            print(f"⏳ Tentativa {i+1}/{retries} falhou para '{db_name}': {e}")
            time.sleep(delay)
    raise Exception(f"❌ Não foi possível conectar ao banco '{db_name}' após {retries} tentativas.")

def recreate_tables(engine, base, db_name):
    print(f"🧹 Dropando todas as tabelas no banco {db_name}...")
    base.metadata.drop_all(bind=engine)
    print(f"✅ Tabelas antigas no banco {db_name} apagadas!")

    print(f"🛠️  Criando tabelas no banco {db_name}...")
    base.metadata.create_all(bind=engine)
    print(f"✅ Tabelas criadas no banco {db_name} com sucesso!")

def seed_data(engine, db_name):
    session = Session(bind=engine)
    try:
        print(f"🌱 Inserindo dados de exemplo no banco {db_name}...")

        if db_name == 'users':
            user = User(name="Admin", email="admin@example.com")
            session.add(user)
        elif db_name == 'products':
            product = Product(name="Produto Teste", price=99)
            session.add(product)
        elif db_name == 'orders':
            order = Order(user_id=1, product_id=1)
            session.add(order)

        session.commit()
        print(f"✅ Dados inseridos no banco {db_name} com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao inserir dados de exemplo no banco {db_name}: {e}")
    finally:
        session.close()

def initialize_databases():
    # Esperar pelos bancos de dados
    wait_for_db(engine_users, "users")
    wait_for_db(engine_products, "products")
    wait_for_db(engine_orders, "orders")

    # Recriar as tabelas
    recreate_tables(engine_users, BaseUsers, "users")
    recreate_tables(engine_products, BaseProducts, "products")
    recreate_tables(engine_orders, BaseOrders, "orders")

    # Inserir dados de exemplo
    seed_data(engine_users, "users")
    seed_data(engine_products, "products")
    seed_data(engine_orders, "orders")

if __name__ == "__main__":
    initialize_databases()

