from locust import HttpUser, task, between
import random
import logging

logging.basicConfig(level=logging.INFO)

class EcommerceUser(HttpUser):
    # AQUI: definir o host completo, com protocolo e porta
    host = "http://api-composer:8000"
    wait_time = between(1, 3)

    user_id = None
    product_id = None
    order_id = None

    def on_start(self):
        self.user_id = self.create_user()
        self.product_id = self.create_product()

    def create_user(self):
        name = f"user{random.randint(1, 100000)}"
        email = f"{name}@test.com"
        res = self.client.post("/users", json={"name": name, "email": email})
        if res.status_code in (200, 201):
            logging.info(f"User created with id: {res.json()}")
            return res.json().get("id") or res.json().get("user_id")
        else:
            logging.error(f"Failed to create user: {res.status_code} {res.text}")
            return None

    def create_product(self):
        name = f"product{random.randint(1, 100000)}"
        price = round(random.uniform(10, 100), 2)
        quantity = random.randint(1, 10)
        res = self.client.post("/products", json={"name": name, "price": price, "quantity": quantity})
        if res.status_code in (200, 201):
            logging.info(f"Product created with id: {res.json()}")
            return res.json().get("id") or res.json().get("product_id")
        else:
            logging.error(f"Failed to create product: {res.status_code} {res.text}")
            return None

    @task(5)
    def create_order(self):
        if not self.user_id or not self.product_id:
            logging.warning("Skipping create_order because user_id or product_id is None")
            return
        order = {
            "user_id": self.user_id,
            "products": [{"product_id": self.product_id, "quantity": random.randint(1, 5)}]
        }
        res = self.client.post("/orders", json=order)
        if res.status_code in (200, 201):
            logging.info(f"Order created: {res.json()}")
            self.order_id = res.json().get("id") or res.json().get("order_id")
        else:
            logging.error(f"Failed to create order: {res.status_code} {res.text}")

    @task(2)
    def get_order(self):
        if self.order_id:
            res = self.client.get(f"/orders/{self.order_id}")
            if res.status_code != 200:
                logging.error(f"Failed to get order {self.order_id}: {res.status_code} {res.text}")

    @task(2)
    def get_user_orders(self):
        if self.user_id:
            res = self.client.get(f"/users/{self.user_id}/orders")
            if res.status_code != 200:
                logging.error(f"Failed to get orders for user {self.user_id}: {res.status_code} {res.text}")

    @task(1)
    def list_users(self):
        res = self.client.get("/users")
        if res.status_code != 200:
            logging.error(f"Failed to list users: {res.status_code} {res.text}")

    @task(1)
    def list_products(self):
        res = self.client.get("/products")
        if res.status_code != 200:
            logging.error(f"Failed to list products: {res.status_code} {res.text}")

    @task(1)
    def list_orders(self):
        res = self.client.get("/orders")
        if res.status_code != 200:
            logging.error(f"Failed to list orders: {res.status_code} {res.text}")


