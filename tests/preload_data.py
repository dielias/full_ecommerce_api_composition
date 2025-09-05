import httpx
import random
import asyncio
import json
import argparse
import uuid

# URLs dos microserviços diretamente
USERS_SERVICE_URL = "http://localhost:8001"
PRODUCTS_SERVICE_URL = "http://localhost:8002"
ORDERS_SERVICE_URL = "http://localhost:8003"

async def create_user(client):
    name = f"User{random.randint(1, 100000)}"
    email = f"user_{uuid.uuid4()}@test.com"
    payload = {"name": name, "email": email}
    try:
        res = await client.post(f"{USERS_SERVICE_URL}/users", json=payload)
        if res.status_code in (200, 201):
            data = res.json()
            print(f"[OK] Usuário criado: {data}")
            return data
        else:
            print(f"[ERRO] Falha ao criar usuário {name}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao criar usuário {name}: {e}")

async def create_product(client):
    name = f"Product{random.randint(1, 100000)}"
    price = round(random.uniform(10, 100), 2)
    quantity = random.randint(1, 20)
    payload = {"name": name, "price": price, "quantity": quantity}
    try:
        res = await client.post(f"{PRODUCTS_SERVICE_URL}/products", json=payload)
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
    payload = {
        "user_id": int(user_id),
        "products": [{"product_id": int(product_id), "quantity": quantity}]
    }
    try:
        res = await client.post(f"{ORDERS_SERVICE_URL}/orders", json=payload)
        if res.status_code in (200, 201):
            data = res.json()
            print(f"[OK] Pedido criado: {data}")
            return data
        else:
            print(f"[ERRO] Falha ao criar pedido para usuário {user_id} e produto {product_id}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao criar pedido para usuário {user_id} e produto {product_id}: {e}")

async def main(num_users, num_products, num_orders):
    async with httpx.AsyncClient(timeout=10.0) as client:
        print("Criando usuários...")
        users = await asyncio.gather(*[create_user(client) for _ in range(num_users)])
        users = [u for u in users if u is not None and "id" in u]

        print("Criando produtos...")
        products = await asyncio.gather(*[create_product(client) for _ in range(num_products)])
        products = [p for p in products if p is not None and "product_id" in p]

        if not users or not products:
            print("[ERRO] Nenhum usuário ou produto válido criado. Abortando criação de pedidos.")
            return

        print("Criando pedidos...")
        order_tasks = []
        for _ in range(num_orders):
            user = random.choice(users)
            product = random.choice(products)
            order_tasks.append(create_order(client, user["id"], product["product_id"]))

        orders = await asyncio.gather(*order_tasks)
        orders = [o for o in orders if o is not None and "order_id" in o]

        # Salva IDs em JSON
        with open("preload_ids.json", "w") as f:
            json.dump({
                "users": [{"id": u["id"]} for u in users],
                "products": [{"id": p["product_id"]} for p in products],
                "orders": [{"id": o["order_id"]} for o in orders]
            }, f, indent=2)

        print("[OK] Arquivo preload_ids.json gerado.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pré-carregar dados de teste diretamente nos microserviços.")
    parser.add_argument("--users", type=int, default=10, help="Número de usuários a criar")
    parser.add_argument("--products", type=int, default=10, help="Número de produtos a criar")
    parser.add_argument("--orders", type=int, default=20, help="Número de pedidos a criar")
    args = parser.parse_args()

    asyncio.run(main(args.users, args.products, args.orders))









