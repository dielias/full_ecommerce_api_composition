#Teste 2: Consulta dados cruzados de serviços
from locust import HttpUser, task, between

class QueryTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_orders_with_details(self):
        # Chama endpoint que retorna pedidos com dados de usuário e produto
        response = self.client.get("/pedidos/detalhes/")
        print(f"Resposta pedidos detalhados: {response.status_code}")
        # Opcional: checar se o JSON está ok
        data = response.json()
        if not data or "usuario" not in data[0] or "produto" not in data[0]:
            print("Dados incompletos ou inválidos")
