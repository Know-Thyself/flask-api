from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)


# Get stores route/endpoint
@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


# Get a specific store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 201
    except KeyError:
        abort(404, message="Store not found!")


# Get items from a specific store
@app.get("/store/<string:name>/items")
def get_store_items(name):
    store = list(filter(lambda s: s["name"] == name, stores))
    return (
        ({"store_items": store[0]["items"]}, 201)
        if store[0]["items"]
        else ({"message": "No items found in the store!"}, 404)
    )


# Create a store
@app.post("/store")
def create_store():
    store = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store, "store_id": store_id}
    stores[store_id] = new_store
    return new_store, 201


# Adding item
@app.post("/item")
def add_item():
    item = request.get_json()
    if not "store_id" in item or not "name" in item or not "price" in item:
        abort(
            400,
            message="Bad request! Please ensure store_id, name and price are included in the JSON payload",
        )
    if item["name"] in items.values() or item["store_id"] in items.values():
        abort(400, message="Bad request! Item already exists.")
    item_id = uuid.uuid4().hex
    new_item = {**item, "item_id": item_id}
    items[item_id] = new_item

    return new_item


# if __name__ == "__main__":
#     app.run(debug=True)
