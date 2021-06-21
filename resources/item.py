from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every Item must have a store_id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":f"item {name} not found"},404


    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item: return {"message": f"item {name} already exists"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured while inserting in db"},500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "item Deleted"}


class Itemlist(Resource):
    def get(self):       #list(map(labda x:x.json(),ItemModel.query.all()))
        return {"items":[item.json() for item in ItemModel.query.all()]}