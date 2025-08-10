#Teste 5: Mede latência das operações
from locust import HttpUser, task, between

class LatencyTestUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def get_user_by_id(self):
        user_id = 1  # pode trocar para um ID válido na sua base
        response = self.client.get(f"/usuarios/{user_id}")
        print(f"Status: {response.status_code}")
