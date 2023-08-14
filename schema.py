from marshmallow import Schema, fields

class ItemSchema(Schema):
    item_id = fields.Str(dump_only=True)
    item_name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdate(Schema):
    item_name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    store_id = fields.Str(dump_only=True)
    store_name = fields.Str(required=True)
    