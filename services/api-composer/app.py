from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import List, Dict

# URLs dos microserviços
USERS_SERVICE_URL = "http://users:8001"
PRODUCTS_SERVICE_URL = "http://products:8002"
ORDERS_SERVICE_URL = "http://orders:8003"

app = FastAPI()

# Modelo Pydantic para a estrutura da resposta
class Product(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int

class OrderResponse(BaseModel):
    order_id: int
    user: Dict
    products: List[Product]
    total: float

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    async with httpx.AsyncClient(timeout=10.0) as client:  # Timeout de 10 segundos
        try:
            # Chama o serviço de pedidos
            order_response = await client.get(f"{ORDERS_SERVICE_URL}/orders/{order_id}")
            if order_response.status_code != 200:
                raise HTTPException(status_code=order_response.status_code, detail="Order service is not available")
            order_data = order_response.json()

            # Chama o serviço de usuários
            user_response = await client.get(f"{USERS_SERVICE_URL}/users/{order_data['user_id']}")
            if user_response.status_code != 200:
                raise HTTPException(status_code=user_response.status_code, detail="User service is not available")
            user_data = user_response.json()

            # Chama o serviço de produtos
            products = []
            for product_id in order_data['products']:
                product_response = await client.get(f"{PRODUCTS_SERVICE_URL}/products/{product_id}")
                if product_response.status_code != 200:
                    raise HTTPException(status_code=product_response.status_code, detail="Product service is not available")
                product_data = product_response.json()
                products.append(product_data)

            # Calcula o total
            total = sum(p["price"] * p["quantity"] for p in products)

            return OrderResponse(
                order_id=order_data["order_id"],
                user=user_data,
                products=[Product(**product) for product in products],
                total=total
            )

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while connecting to services: {str(e)}")
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Missing expected data: {str(e)}")



