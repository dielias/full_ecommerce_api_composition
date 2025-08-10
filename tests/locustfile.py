import json
import random
from locust import HttpUser, task, between

# Carrega os IDs do arquivo gerado pelo preload_data.py
with open("preload_ids.json") as f:
    preload_data = json.load(f)

ORDER_IDS = [order["id"] for order in preload_data.get("orders", [])]
USER_IDS = [user["id"] for user in preload_data.get("users", [])]

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_order(self):
        if not ORDER_IDS:
            return
        order_id = random.choice(ORDER_IDS)
        with self.client.get(f"/orders/{order_id}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Erro ao buscar pedido {order_id}")

    @task(1)
    def get_user_orders(self):
        if not USER_IDS:
            return
        user_id = random.choice(USER_IDS)
        with self.client.get(f"/users/{user_id}/orders", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Erro ao buscar pedidos do usuário {user_id}")



