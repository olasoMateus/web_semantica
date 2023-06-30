from flask import Flask
from flask_restx import Api, Resource

from src.server.instance import server

app = server.app
api = server.api

ander = {'hello': 'world'}

@api.route('/abba')
class UrbanIot(Resource):
    def get(self, ):
        return ander

    def post(self):
        response = api.payload
        ander.update(response)
        return response, 200

