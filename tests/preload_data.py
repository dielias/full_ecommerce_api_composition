import httpx
import random
import asyncio
from faker import Faker
import json

USERS_API_URL = "http://localhost:8001"
PRODUCTS_API_URL = "http://localhost:8002"
ORDERS_API_URL = "http://localhost:8003"

faker = Faker()


async def delete_old_data(client):
    print("Deletando dados antigos...")

    # Deleta pedidos antigos
    try:
        res_orders = await client.get(f"{ORDERS_API_URL}/orders")
        if res_orders.status_code == 200:
            orders = res_orders.json()
            for order in orders:
                order_id = order.get("order_id") or order.get("id")
                res_del = await client.delete(f"{ORDERS_API_URL}/orders/{order_id}")
                if res_del.status_code == 200:
                    print(f"[OK] Pedido {order_id} deletado")
    except Exception as e:
        print(f"[ERRO] Falha ao deletar pedidos antigos: {e}")

    # Deleta produtos antigos
    try:
        res_products = await client.get(f"{PRODUCTS_API_URL}/products")
        if res_products.status_code == 200:
            products = res_products.json()
            for product in products:
                product_id = product.get("product_id") or product.get("id")
                res_del = await client.delete(f"{PRODUCTS_API_URL}/products/{product_id}")
                if res_del.status_code == 200:
                    print(f"[OK] Produto {product_id} deletado")
    except Exception as e:
        print(f"[ERRO] Falha ao deletar produtos antigos: {e}")

    # Deleta usuários antigos
    try:
        res_users = await client.get(f"{USERS_API_URL}/users")
        if res_users.status_code == 200:
            users = res_users.json()
            for user in users:
                user_id = user.get("id") or user.get("user_id")
                res_del = await client.delete(f"{USERS_API_URL}/users/{user_id}")
                if res_del.status_code == 200:
                    print(f"[OK] Usuário {user_id} deletado")
    except Exception as e:
        print(f"[ERRO] Falha ao deletar usuários antigos: {e}")


async def create_user(client, user_number):
    name = faker.name()
    email = faker.unique.email()
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
    name = faker.word().capitalize()
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
    payload = {
        "user_id": user_id,
        "products": [
            {"product_id": int(product_id), "quantity": int(quantity)}
        ]
    }
    print(f"[DEBUG] Criando pedido: {json.dumps(payload)}")  # log do payload
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
        await delete_old_data(client)

        print("Criando usuários...")
        user_results = await asyncio.gather(*[create_user(client, i) for i in range(quantidade_usuarios)])
        print("Criando produtos...")
        product_results = await asyncio.gather(*[create_product(client, i) for i in range(quantidade_produtos)])

        users = [u for u in user_results if u is not None and ("id" in u or "user_id" in u)]
        products = [p for p in product_results if p is not None and ("product_id" in p or "id" in p)]

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
            user_id = user.get("id") or user.get("user_id")
            product_id = product.get("product_id") or product.get("id")
            order_tasks.append(create_order(client, user_id, product_id))

        order_results = await asyncio.gather(*order_tasks)

        with open("preload_ids.json", "w") as f:
            json.dump({
                "users": [{"id": u.get("id") or u.get("user_id")} for u in users],
                "products": [{"id": p.get("product_id") or p.get("id")} for p in products],
                "orders": [{"id": o.get("order_id") or o.get("id")} for o in order_results if o is not None]
            }, f, indent=2)

        print("[OK] Arquivo preload_ids.json gerado.")


if __name__ == "__main__":
    asyncio.run(main())
