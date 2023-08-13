from flask import Flask, request

app = Flask(__name__)

# Temp data
stores = [
    {
        "name": "My Store",
        "items": [
            {"name": "chair", "price": "£29.99"},
            {"name": "table", "price": "£49.99"},
        ],
    }
]


# Get stores route/endpoint
@app.get("/stores")
def get_stores():
    return {"stores": stores}


# Get a specific store
@app.get("/store/<string:name>")
def get_store(name):
    store = list(filter(lambda s: s["name"] == name, stores))
    return (store, 201) if store else ({"message": "Store not found!"}, 404)


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
    new_store = {"name": store["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


# Adding item
@app.post("/store/<string:name>/item")
def add_item(name):
    item = request.get_json()
    new_item = {"name": item["name"], "price": item["price"]}
    for store in stores:
        if store["name"] == name:
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found!"}, 404


# if __name__ == "__main__":
#     app.run(debug=True)
