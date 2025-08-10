#Teste 3: Atualização concorrente
from locust import HttpUser, task, between

class ConcurrentUpdateUser(HttpUser):
    wait_time = between(0.5, 1)

    def on_start(self):
        # Criar um produto para teste (pode ser feito antes, se preferir)
        resp = self.client.post("/produtos/", json={"nome": "Produto Concorrente", "estoque": 10})
        self.product_id = resp.json().get("id")

    @task
    def reduce_stock(self):
        payload = {
            "produto_id": self.product_id,
            "quantidade": 1
        }
        # Endpoint que reduz estoque (pode ser update ou pedido que diminui estoque)
        response = self.client.post("/produtos/reduzir_estoque/", json=payload)
        print(f"Resposta redução estoque: {response.status_code}")
