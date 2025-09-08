import json
import random
import uuid
from locust import HttpUser, task, between

# Carrega IDs de dados pré-carregados para tarefas de leitura
try:
    with open("preload_ids.json") as f:
        preload_data = json.load(f)
    # Acessando os IDs com a chave 'id' para manter a consistência
    ORDER_IDS = [order["id"] for order in preload_data.get("orders", [])]
    USER_IDS = [user["id"] for user in preload_data.get("users", [])]
except (FileNotFoundError, KeyError) as e:
    print(f"Erro ao carregar preload_ids.json: {e}. Tarefas de leitura podem falhar.")
    ORDER_IDS = []
    USER_IDS = []

class ApiCompositionUser(HttpUser):
    # O Locust se conecta ao Gateway de API
    host = "http://api-composer:8000"

    wait_time = between(1, 3)

    user_id = None
    product_id = None

    def on_start(self):
        """
        No teste de leitura, não é necessário criar dados em cada 'on_start'.
        A criação de dados é feita pelo script 'preload_data.py'.
        """
        # A lógica de criação de dados foi removida daqui para manter o foco em testes de leitura.
        pass

    @task(3)
    def create_order(self):
        """
        Esta tarefa foi removida, pois os dados são pré-carregados.
        """
        pass
    
    @task(3)
    def get_order(self):
        """
        Busca um pedido existente por ID, usando os dados pré-carregados.
        """
        if not ORDER_IDS:
            return
        order_id = random.choice(ORDER_IDS)
        with self.client.get(f"/orders/{order_id}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Erro ao buscar pedido {order_id}: {response.text}")

    @task(1)
    def get_user_orders(self):
        """
        Busca todos os pedidos de um usuário, usando os dados pré-carregados.
        """
        if not USER_IDS:
            return
        user_id = random.choice(USER_IDS)
        with self.client.get(f"/users/{user_id}/orders", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Erro ao buscar pedidos do usuário {user_id}: {response.text}")








