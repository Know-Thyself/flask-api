import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

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

    def post(self):
        store = request.get_json()
        if not "store_name" in store:
            abort(
                400,
                message="Bad request! Please make sure to include store_name in JSON payload.",
            )
        if "store_name" in stores:
            abort(400, message="Store already exists.")
        store_id = uuid.uuid4().hex
        new_store = {**store, "store_id": store_id}
        stores[store_id] = new_store
        return new_store, 201
