from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import List, Dict

# URLs dos microserviços
USERS_SERVICE_URL = "http://users:8001"
PRODUCTS_SERVICE_URL = "http://products:8002"
ORDERS_SERVICE_URL = "http://orders:8003"

app = FastAPI()

# Modelos Pydantic para as respostas
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

class UserOrdersResponse(BaseModel):
    order_id: int
    products: List[Product]
    total: float

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            order_response = await client.get(f"{ORDERS_SERVICE_URL}/orders/{order_id}")
            if order_response.status_code != 200:
                raise HTTPException(status_code=order_response.status_code, detail="Order service is not available")
            order_data = order_response.json()

            user_response = await client.get(f"{USERS_SERVICE_URL}/users/{order_data['user_id']}")
            if user_response.status_code != 200:
                raise HTTPException(status_code=user_response.status_code, detail="User service is not available")
            user_data = user_response.json()

            products = []
            for prod in order_data['products']:
                product_id = prod['product_id']
                quantity = prod['quantity']
                product_response = await client.get(f"{PRODUCTS_SERVICE_URL}/products/{product_id}")
                if product_response.status_code != 200:
                    raise HTTPException(status_code=product_response.status_code, detail="Product service is not available")
                product_data = product_response.json()
                product_data['quantity'] = quantity
                products.append(product_data)

            total = sum(p["price"] * p["quantity"] for p in products)

            return OrderResponse(
                order_id=order_data["order_id"],
                user=user_data,
                products=[Product(**p) for p in products],
                total=total
            )

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Service connection error: {str(e)}")
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Missing expected data: {str(e)}")

@app.get("/users/{user_id}/orders", response_model=List[UserOrdersResponse])
async def get_user_orders(user_id: int):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            orders_response = await client.get(f"{ORDERS_SERVICE_URL}/orders")
            if orders_response.status_code != 200:
                raise HTTPException(status_code=orders_response.status_code, detail="Order service is not available")
            orders_data = orders_response.json()

            user_orders = [order for order in orders_data if int(order["user_id"]) == int(user_id)]

            detailed_orders = []
            for order in user_orders:
                products = []
                for prod in order['products']:
                    product_id = prod['product_id']
                    quantity = prod['quantity']
                    product_response = await client.get(f"{PRODUCTS_SERVICE_URL}/products/{product_id}")
                    if product_response.status_code != 200:
                        raise HTTPException(status_code=product_response.status_code, detail="Product service is not available")
                    product_data = product_response.json()
                    product_data['quantity'] = quantity
                    products.append(product_data)

                total = sum(p["price"] * p["quantity"] for p in products)

                detailed_orders.append(UserOrdersResponse(
                    order_id=order["order_id"],
                    products=[Product(**p) for p in products],
                    total=total
                ))

            return detailed_orders

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Service connection error: {str(e)}")
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Missing expected data: {str(e)}")
