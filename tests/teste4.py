#Teste 4: Simula falha do banco de dados
from locust import HttpUser, task, between
from requests.exceptions import ConnectionError

class SimulateDbFailureUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def call_api_with_possible_failure(self):
        try:
            response = self.client.get("/produtos/")
            print(f"Status: {response.status_code}")
        except ConnectionError:
            print("Falha na conexão - banco possivelmente fora")
