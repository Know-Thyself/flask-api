from flask import Flask

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


# Stores route/endpoint
@app.get("/stores")
def get_stores():
    return {"stores": stores}
