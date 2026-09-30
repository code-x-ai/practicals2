import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Benchmark Target API")

items = {}


class Item(BaseModel):
    name: str
    price: int


@app.get("/")
def root():
    return {"message": "Benchmark Target API is running"}


@app.get("/fast")
def fast_endpoint():
    """A lightweight endpoint. Returns immediately."""
    return {
        "status": "ok",
        "type": "fast",
        "data": [1, 2, 3, 4, 5]
    }
# pip install fastapi uvicorn pydantic locust
# uvicorn target_api:app --port 8000
# locust -f locustfile.py --host http://127.0.0.1:8000
@app.get("/slow")
def slow_endpoint():
    """Simulates a slow database query taking 500 milliseconds."""
    time.sleep(0.5)
    return {"status": "ok", "type": "slow"}


@app.post("/items")
def create_item(item: Item):
    """A write endpoint that validates input and stores it."""
    item_id = len(items) + 1
    items[item_id] = item.dict()
    return {"id": item_id, "item": item.dict()}
