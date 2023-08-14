import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schema import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Store not found!")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/stores")
class StoresList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    def post(self, new_store):
        store = request.get_json()
        for store in stores.values():
            if new_store["store_name"] == store["store_name"]:
                abort(400, message="Store already exists.")
        store_id = uuid.uuid4().hex
        store = {**new_store, "store_id": store_id}
        stores[store_id] = store
        return store, 201
