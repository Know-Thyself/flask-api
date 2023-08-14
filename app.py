from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)


# Get all stores route/endpoint
@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


# Get all items
@app.get("/items")
def get_items():
    return {"items": list(items.values())}


# Get a specific store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store not found!")


# Get a specific item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found!")


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


# Updating item
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # There's  more validation to do here!
    # Like making sure price is a number, and also both items are optional
    if not "price" in item_data or not "name" in item_data:
        abort(
            400,
            message="Bad request. Please ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]
        # https://blog.teclado.com/python-dictionary-merge-update-operators/
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found.")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
