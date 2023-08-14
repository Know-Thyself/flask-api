import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found!")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
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


@blp.route("/items")
class ItemsList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item = request.get_json()
        print(item)
        if not "item_name" in item:
            abort(
                400,
                message="Bad request! Please make sure to include item_name in JSON payload.",
            )
        if "item_name" in items:
            abort(400, message="Item already exists.")
        item_id = uuid.uuid4().hex
        new_store = {**item, "item_id": item_id}
        items[item_id] = new_store
        return new_store, 201
