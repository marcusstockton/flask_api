from flask_restful import Api, Resource
from flask import Blueprint
from .models import Address
from flask import request, jsonify
from .schemas import AddressSchema
from flask_jwt_extended import jwt_required

address_profile = Blueprint('addressProfile', __name__)
api = Api(address_profile)

class AddressCollection(Resource):
    # Get all addresses
    def get(self):
        items = Address.get_all()
        schema = AddressSchema(many=True)
        return schema.jsonify(items)


    # Create new address
    @jwt_required
    def post(self):
        req_data = request.get_json()
        schema = AddressSchema()
        data = schema.load(req_data)
        new_item = data.data
        Address.create_address(new_item)

        result = schema.dump(new_item).data
        
        return (result, 201)


class AddressItem(Resource):
    def get(self, id):
        item = Address.get_by_id(id)
        schema = AddressSchema()
        return schema.jsonify(item)
    
    @jwt_required
    def put(self, id):
        pass

    @jwt_required
    def delete(self, id):
        pass



api.add_resource(AddressCollection, '/api/address')
api.add_resource(AddressItem, '/api/address/<int:id>')

