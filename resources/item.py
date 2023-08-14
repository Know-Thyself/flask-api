import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schema import ItemSchema, ItemUpdate

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

    @blp.arguments(ItemUpdate)
    def put(self, item_data, item_id):
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

    @blp.arguments(ItemSchema)
    def post(self, new_item):
        for item in items.values():
            if (
                new_item["item_name"] == item["item_name"]
                and new_item["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")
        item_id = uuid.uuid4().hex
        item = {**new_item, "item_id": item_id}
        items[item_id] = item
        return item, 201
