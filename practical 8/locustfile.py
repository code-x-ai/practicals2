# locustfile.py
import random
from locust import HttpUser, task, between


class APIUser(HttpUser):
    """Each instance represents one virtual user."""

    wait_time = between(1, 2)

    def on_start(self):
        """Called when a virtual user starts."""
        self.client.get("/")

    @task(6)
    def call_fast_endpoint(self):
        """Most frequent task — lightweight endpoint."""
        self.client.get("/fast")

    @task(3)
    def create_item(self):
        """Write endpoint with validation."""
        payload = {
            "name": f"item-{random.randint(1, 10000)}",
            "price": random.randint(10, 500)
        }
        self.client.post("/items", json=payload)

    @task(1)
    def call_slow_endpoint(self):
        """Least frequent task — slow endpoint (bottleneck)."""
        self.client.get("/slow")