#Teste 1: Cria dados relacionados 
from locust import HttpUser, task, between

class SimpleTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_related_data(self):
        # Criar usuário
        user_resp = self.client.post("/usuarios/", json={"nome": "Usuário Teste"})
        user_id = user_resp.json().get("id")

        # Criar produto
        product_resp = self.client.post("/produtos/", json={"nome": "Produto Teste", "estoque": 100})
        product_id = product_resp.json().get("id")

        # Criar pedido com usuário e produto
        order_payload = {
            "usuario_id": user_id,
            "produto_id": product_id,
            "quantidade": 1
        }
        order_resp = self.client.post("/pedidos/", json=order_payload)

        # Opcional: imprimir resultado para debug
        print(f"Pedido criado: {order_resp.status_code} - {order_resp.text}")
