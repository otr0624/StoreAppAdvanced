from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from models.item import ItemModel
from schemas.item import ItemSchema

ITEM_NOT_FOUND = "Item not found."
NAME_ALREADY_EXISTS = "An item with name {} already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_DELETED = "Item deleted."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Item(Resource):
    @classmethod
    @jwt_required
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump()
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return (
                {"message": NAME_ALREADY_EXISTS.format(name)},
                400,
            )

        item_json = request.get_json()
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}
        return {"message": ITEM_NOT_FOUND}

    @classmethod
    @jwt_required
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item is None:
            item.price = item_json["price"]
        else:
            item_json["name"] = name

            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200


# ADMIN-ONLY VERSION OF DELETE ENDPOINT (IMPORT get_jwt_claims AT TOP):
#     @jwt_required
#     def delete(self, name):
#         claims = get_jwt_claims()
#         if not claims['is_admin']:
#             return {'message': 'Admin privilege required'}, 401
#         item = ItemModel.find_by_name(name)
#         if item:
#             item.delete_from_db()
#
#         return {'message': 'Item deleted'}

# JWT-OPTIONAL VERSION OF ITEMS ENDPOINT (IMPORT jwt_optional, get_jwt_identity AT TOP):
#
# class ItemList(Resource):
#     @jwt_optional
#     def get(self):
#         user_id = get_jwt_identity()
#         items = [item.json() for item in ItemModel.find_all()]
#         if user_id:
#             return {'items': items}, 200
#         return {
#             'items': [item['name'] for item in items],
#             'message': 'More data available if you log in.'
#         }, 200
