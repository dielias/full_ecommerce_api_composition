import random
from locust import HttpUser, task, between

# URLs base das APIs
ORDERS_API_URL = "http://localhost:8003"
USERS_API_URL = "http://localhost:8001"

# Listas de IDs
ORDER_IDS = []
USER_IDS = []

def carregar_ids():
    """Carrega IDs reais direto das APIs"""
    import requests

    # Buscar todos os pedidos
    try:
        resp_orders = requests.get(f"{ORDERS_API_URL}/orders", timeout=5)
        if resp_orders.status_code == 200:
            orders_data = resp_orders.json()
            # Garante que pega order_id certo
            for o in orders_data:
                oid = o.get("order_id") or o.get("id")
                if oid:
                    ORDER_IDS.append(oid)
            print(f"[INFO] {len(ORDER_IDS)} pedidos carregados")
        else:
            print(f"[ERRO] Falha ao buscar pedidos: {resp_orders.status_code}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao buscar pedidos: {e}")

    # Buscar todos os usuários
    try:
        resp_users = requests.get(f"{USERS_API_URL}/users", timeout=5)
        if resp_users.status_code == 200:
            users_data = resp_users.json()
            for u in users_data:
                uid = u.get("id") or u.get("user_id")
                if uid:
                    USER_IDS.append(uid)
            print(f"[INFO] {len(USER_IDS)} usuários carregados")
        else:
            print(f"[ERRO] Falha ao buscar usuários: {resp_users.status_code}")
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao buscar usuários: {e}")

# Carrega IDs no início
carregar_ids()

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

