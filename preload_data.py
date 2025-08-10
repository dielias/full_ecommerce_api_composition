import httpx
import random
import asyncio
from faker import Faker

USERS_API_URL = "http://localhost:8001"
PRODUCTS_API_URL = "http://localhost:8002"
ORDERS_API_URL = "http://localhost:8003"

faker = Faker()

async def create_user(client, user_number):
    name = faker.name()  # Nome realista, ex: "Ana Silva"
    email = faker.unique.email()  # Email único e realista
    payload = {"name": name, "email": email}
    try:
        res = await client.post(f"{USERS_API_URL}/users", json=payload)
        if res.status_code in (200, 201):
            data = res.json()
            print(f"[OK] Usuário criado: {data}")
            return data
        else:
            print(f"[ERRO] Falha ao criar usuário {name}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao criar usuário {name}: {e}")

async def create_product(client, product_number):
    name = faker.word().capitalize()  # Palavra realista simples, ex: "Laptop"
    price = round(random.uniform(10, 100), 2)
    quantity = random.randint(1, 20)
    payload = {"name": name, "price": price, "quantity": quantity}
    try:
        res = await client.post(f"{PRODUCTS_API_URL}/products", json=payload)
        if res.status_code in (200, 201):
            data = res.json()
            print(f"[OK] Produto criado: {data}")
            return data
        else:
            print(f"[ERRO] Falha ao criar produto {name}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao criar produto {name}: {e}")

async def create_order(client, user_id, product_id):
    quantity = random.randint(1, 5)
    payload = {"user_id": user_id, "products": [{"product_id": product_id, "quantity": quantity}]}
    try:
        res = await client.post(f"{ORDERS_API_URL}/orders", json=payload)
        if res.status_code in (200, 201):
            data = res.json()
            print(f"[OK] Pedido criado: {data}")
            return data
        else:
            print(f"[ERRO] Falha ao criar pedido para usuário {user_id} e produto {product_id}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao criar pedido para usuário {user_id} e produto {product_id}: {e}")

async def main():
    quantidade_usuarios = int(input("Quantidade de usuários (N): "))
    quantidade_produtos = int(input("Quantidade de produtos (M): "))
    quantidade_pedidos = int(input("Quantidade de pedidos (K): "))

    async with httpx.AsyncClient(timeout=10.0) as client:
        user_results = await asyncio.gather(*[create_user(client, i) for i in range(quantidade_usuarios)])
        product_results = await asyncio.gather(*[create_product(client, i) for i in range(quantidade_produtos)])

        users = [u for u in user_results if u is not None and "id" in u]
        products = [p for p in product_results if p is not None and "id" in p]

        if not users:
            print("[ERRO] Nenhum usuário válido foi criado. Abortando criação de pedidos.")
            return
        if not products:
            print("[ERRO] Nenhum produto válido foi criado. Abortando criação de pedidos.")
            return

        order_tasks = []
        for _ in range(quantidade_pedidos):
            user = random.choice(users)
            product = random.choice(products)
            order_tasks.append(create_order(client, user["id"], product["product_id"]))

        await asyncio.gather(*order_tasks)

if __name__ == "__main__":
    asyncio.run(main())


