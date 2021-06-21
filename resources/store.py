from flask_restful import Resource,reqparse
from models.store import StoreModel


class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":f"store {name} not found"},404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message":f"store {name} Already exists"},400

        store = StoreModel(name)
        store.save_to_db()

        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.delete_from_db()

        return {"message":f"store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}