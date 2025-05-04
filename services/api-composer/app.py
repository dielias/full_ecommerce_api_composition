from fastapi import FastAPI
import httpx

# URLs dos microserviços
USERS_SERVICE_URL = "http://users:8001"
PRODUCTS_SERVICE_URL = "http://products:8002"
ORDERS_SERVICE_URL = "http://orders:8003"

app = FastAPI()

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    async with httpx.AsyncClient() as client:
        # Chama o serviço de pedidos
        order_response = await client.get(f"{ORDERS_SERVICE_URL}/orders/{order_id}")
        order_data = order_response.json()

        # Chama o serviço de usuários
        user_response = await client.get(f"{USERS_SERVICE_URL}/users/{order_data['user_id']}")
        user_data = user_response.json()

        # Chama o serviço de produtos
        products = []
        for product_id in order_data['products']:
            product_response = await client.get(f"{PRODUCTS_SERVICE_URL}/products/{product_id}")
            product_data = product_response.json()
            products.append(product_data)

        # Combina as respostas
        return {
            "order_id": order_data["order_id"],
            "user": user_data,
            "products": products,
            "total": sum(p["price"] * p["quantity"] for p in products)
        }


